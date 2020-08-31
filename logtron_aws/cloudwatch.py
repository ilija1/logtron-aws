import json
import threading
import time
from logging import Handler
from uuid import uuid4

import boto3


class CloudWatchHandler(Handler):
    MAX_BATCH_SIZE = 1048576
    EXTRA_BYTES_PER_EVENT = 26
    REQUESTS_PER_SECOND = 5

    def __init__(self, context, logs_client=None, interval_sec=1.0, retention_days=None):
        super(CloudWatchHandler, self).__init__()
        self.context = context
        self.batch = []
        self.batch_size = 0
        self.interval_sec = max(interval_sec, 1.0 / CloudWatchHandler.REQUESTS_PER_SECOND)
        self.retention_days = retention_days
        self.client = logs_client if logs_client is not None else boto3.client("logs")
        self.log_group = self.context["id"]
        self.sequence_token = None

        self.__create_log_group()
        self.__create_log_stream()

        thread = threading.Thread(target=self.__timed_submit, args=())
        thread.daemon = True
        thread.start()

    def __create_log_group(self):
        exists = False
        paginator = self.client.get_paginator("describe_log_groups")
        for i in paginator.paginate(logGroupNamePrefix=self.log_group):
            if len(i["logGroups"]) > 0:
                exists = True
                break

        if not exists:
            self.client.create_log_group(
                logGroupName=self.log_group,
                tags={
                    "CreatedBy": "logtron",
                    "Created": str(int((time.time() * 1000))),
                },
            )
            if self.retention_days is not None:
                self.client.put_retention_policy(logGroupName=self.log_group, retentionInDays=self.retention_days)

    def __create_log_stream(self):
        self.log_stream = "logtron-{}".format(str(uuid4()))
        self.client.create_log_stream(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
        )

    def __timed_submit(self):
        while True:
            self.__submit_batch()
            time.sleep(self.interval_sec)

    def __submit_batch(self):
        self.acquire()
        if len(self.batch) == 0:
            self.release()
            return

        args = {
            "logGroupName": self.log_group,
            "logStreamName": self.log_stream,
            "logEvents": self.batch,
        }
        if self.sequence_token is not None:
            args["sequenceToken"] = self.sequence_token

        response = self.client.put_log_events(**args)
        self.sequence_token = response["nextSequenceToken"]

        self.batch = []
        self.batch_size = 0
        self.release()

    def emit(self, record):
        json_obj = json.loads(self.format(record))
        timestamp = json_obj["timestamp"]
        json_obj.pop("timestamp")
        message = json.dumps(json_obj)

        log_entry = {
            "timestamp": timestamp,
            "message": message,
        }

        size = len(json.dumps(log_entry)) + CloudWatchHandler.EXTRA_BYTES_PER_EVENT
        if self.batch_size + size > CloudWatchHandler.MAX_BATCH_SIZE:
            self.__submit_batch()

        self.batch_size += size
        self.batch.append(log_entry)

    def flush(self):
        self.__submit_batch()

    def close(self):
        self.__submit_batch()
        super(CloudWatchHandler, self).close()
