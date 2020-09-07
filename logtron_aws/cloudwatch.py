import itertools
import json
import threading
import time
from logging import Handler
from uuid import uuid4

import boto3

from logtron_aws.util import path_get


class CloudWatchHandler(Handler):
    MAX_BATCH_SIZE = 1048576
    EXTRA_BYTES_PER_EVENT = 26
    REQUESTS_PER_SECOND = 5

    def __init__(self, **kwargs):
        super(CloudWatchHandler, self).__init__()
        self.batch = []
        self.batch_size = 0
        self.interval_sec = max(kwargs.get("interval_sec", 1.0), 1.0 / CloudWatchHandler.REQUESTS_PER_SECOND)
        self.retention_days = kwargs.get("retention_days")
        self.client = kwargs.get("logs_client")
        if self.client is None:
            self.client = boto3.client("logs")
        self.emf_namespace = kwargs.get("emf_namespace")
        self.emf_dimensions = kwargs.get("emf_dimensions", [])
        self.emf_metrics = kwargs.get("emf_metrics", [])
        self.emf_header_registered = False
        self.log_group = kwargs.get("log_group")
        self.log_group_initialized = False
        self.log_stream = None
        self.sequence_token = None

        thread = threading.Thread(target=self.__timed_submit, args=())
        thread.daemon = True
        thread.start()

    def __create_log_group(self, record):
        if self.log_group_initialized:
            return

        if self.log_group is None:
            self.log_group, _ = path_get(record, "context.id")

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
        self.log_group_initialized = True

    def __create_log_stream(self, record):
        if not self.log_group_initialized:
            self.__create_log_group(record)

        if self.log_stream is not None:
            return

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

        if not self.emf_header_registered and len(self.emf_metrics) > 0:
            self.client.meta.events.register_first("before-sign.cloudwatch-logs.PutLogEvents", self.__add_emf_header)
            self.emf_header_registered = True

        response = self.client.put_log_events(**args)
        self.sequence_token = response["nextSequenceToken"]

        self.batch = []
        self.batch_size = 0
        self.release()

    def __add_emf_header(self, request, **kwargs):
        request.headers.add_header("x-amzn-logs-format", "json/emf")

    def __get_emf(self, timestamp, record):
        if len(self.emf_metrics) == 0:
            return {}

        metrics = [i for i in self.emf_metrics if i["Name"] in record]
        if len(metrics) == 0:
            return {}

        dimensions = []
        for i in self.emf_dimensions:
            if type(i) != list:
                continue
            dimension = [j for j in i if j in record]
            if len(dimension) > 0:
                dimensions.append(dimension)
        dimensions.sort()
        dimensions = list(k for k, _ in itertools.groupby(dimensions))

        if self.emf_namespace is None:
            self.emf_namespace, _ = path_get(record, "context.id")

        return {
            "_aws": {
                "Timestamp": timestamp,
                "CloudWatchMetrics": [
                    {
                        "Namespace": self.emf_namespace,
                        "Dimensions": dimensions,
                        "Metrics": metrics,
                    }
                ],
            }
        }

    def emit(self, record):
        json_obj = json.loads(self.format(record))
        timestamp = json_obj.pop("timestamp")

        if self.log_stream is None:
            self.__create_log_stream(json_obj)

        # Scrub out any "extra" objects or prefixes
        json_obj = {k.replace("extra_", "") if k.startswith("extra_") else k: v for k, v in json_obj.items()}
        extra = json_obj.pop("extra", {})
        json_obj.update(extra)

        emf = self.__get_emf(timestamp, json_obj)
        json_obj.update(emf)

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
