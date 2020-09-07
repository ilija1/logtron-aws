import logging

import pytest

from logtron_aws import autodiscover


@pytest.mark.skip(reason="integration test -- will submit real logs")
def test_integration():
    config = {
        "handlers": ["logtron_aws.CloudWatchHandler"],
        "CloudWatchHandler": {
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
    logger = autodiscover(refresh=True, config=config)
    logger.info("test_integration", extra={"kind": "test", "value": 123})

    [i.flush() for i in logging.getLogger().handlers]
