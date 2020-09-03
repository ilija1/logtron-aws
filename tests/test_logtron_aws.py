import logging

from logtron_aws import CloudWatchHandler
from logtron_aws import discover_context
from logtron_aws import autodiscover


class MockSTSClientMeta:
    def __init__(self):
        self.region_name = "us-east-1"


class MockSTSClient:
    def __init__(self):
        self.meta = MockSTSClientMeta()

    def get_caller_identity(self):
        return {"Arn": "arn:aws:sts::123456789012:assumed-role/foo/session1"}


def test_context():
    context = discover_context(sts_client=MockSTSClient())
    assert context["id"] is not None


def test_autodiscover():
    config = {
        "handlers": ["logtron.handlers.ConsoleHandler"],
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_autodiscover")


def test_cloudwatch():
    class MockLogsPaginator:
        def __init__(self):
            pass

        def paginate(self, **kwargs):
            return []

    class MockLogsClient:
        def __init__(self):
            pass

        def get_paginator(self, name):
            return MockLogsPaginator()

        def create_log_group(self, **kwargs):
            pass

        def create_log_stream(self, **kwargs):
            pass

        def put_log_events(self, **kwargs):
            return {"nextSequenceToken": "123"}

    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "logtron_aws.CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_cloudwatch")
