import logging

from logtron_aws import CloudWatchHandler
from logtron_aws import discover_context
from logtron_aws import autodiscover
from tests.mocks import MockSTSClient, MockLogsClient, MockLogsPaginator


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

    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_cloudwatch", extra={"test123": 123})

    [i.flush() for i in logging.getLogger().handlers]


def test_cloudwatch_emf():

    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
            "emf_namespace": "bobo",
            "emf_dimensions": ["kind", "smop"],
            "emf_metrics": [
                {
                    "Name": "value",
                    "Unit": "Count",
                },
                {
                    "Name": "fake",
                    "Unit": "Milliseconds",
                },
            ],
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_cloudwatch_emf", extra={"kind": "test", "value": 123})

    [i.flush() for i in logging.getLogger().handlers]


def test_cloudwatch_close():

    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_cloudwatch_close", extra={"test123": 123})

    [i.close() for i in logging.getLogger().handlers]


def test_cloudwatch_existing_log_group():

    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(MockLogsPaginator([{"logGroups": ["foo"]}])),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient())
    )
    logger.info("test_cloudwatch_existing_log_group", extra={"test123": 123})

    [i.flush() for i in logging.getLogger().handlers]
