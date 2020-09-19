import logging

import pytest

from logtron_aws import CloudWatchHandler, autodiscover, discover_context, flush
from tests.mocks import MockLogsClient, MockLogsPaginator, MockSTSClient


def test_context():
    context = discover_context(sts_client=MockSTSClient(), refresh=True)
    assert context["id"] is not None


def test_context_repeat():
    context = discover_context(sts_client=MockSTSClient(), refresh=True)
    assert context["id"] is not None
    context = discover_context(sts_client=MockSTSClient())
    assert context["id"] is not None


def test_autodiscover():
    config = {
        "handlers": ["logtron.handlers.ConsoleHandler"],
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_autodiscover")


def test_empty_config():
    logger = autodiscover(
        refresh=True,
        logs_client=MockLogsClient(),
        discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True),
    )
    logger.info("test_empty_config")
    flush()


def test_autodiscover_repeat():
    config = {
        "handlers": ["logtron.handlers.ConsoleHandler"],
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_autodiscover_repeat1")
    logger = autodiscover()
    logger.info("test_autodiscover_repeat2")


def test_cloudwatch():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch", extra={"test123": 123})

    flush()


def test_cloudwatch_default_handler():
    config = {
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch_default_handler", extra={"test123": 123})

    flush()


def test_cloudwatch_logs_client():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True,
        logs_client=MockLogsClient(),
        config=config,
        discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True),
    )
    logger.info("test_cloudwatch_logs_client", extra={"test123": 123})

    flush()


def test_cloudwatch_no_threading():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True,
        use_threading=False,
        logs_client=MockLogsClient(),
        config=config,
        discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True),
    )
    logger.info("test_cloudwatch_no_threading", extra={"test123": 123})

    flush()


def test_cloudwatch_emf():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
            "emf_namespace": "bobo",
            "emf_dimensions": [["kind", "smop"], ["kind"], "value"],
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
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch_emf", extra={"kind": "test", "value": 123})

    flush()


def test_cloudwatch_emf_detect_ns():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
            "emf_dimensions": [["kind", "smop"], ["kind"], "value"],
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
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch_emf_detect_ns", extra={"kind": "test", "value": 123})

    flush()


def test_cloudwatch_emf_non_flatten():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
            "emf_dimensions": [["kind", "smop"], ["kind"], "value"],
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
        refresh=True,
        flatten=False,
        config=config,
        discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True),
    )
    logger.info("test_cloudwatch_emf_non_flatten", extra={"kind": "test", "value": 123})

    flush()


def test_cloudwatch_sts_client():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(refresh=True, config=config, sts_client=MockSTSClient())
    logger.info("test_cloudwatch_sts_client", extra={"test123": 123})

    flush()


def test_cloudwatch_close():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch_close", extra={"test123": 123})

    for i in logging.getLogger().handlers:
        i.close()


def test_cloudwatch_existing_log_group():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
            "logs_client": MockLogsClient(MockLogsPaginator([{"logGroups": ["foo"]}])),
            "interval_sec": 30,
        },
    }
    logger = autodiscover(
        refresh=True, config=config, discover_context=lambda: discover_context(sts_client=MockSTSClient(), refresh=True)
    )
    logger.info("test_cloudwatch_existing_log_group", extra={"test123": 123})

    flush()
