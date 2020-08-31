__version__ = "0.1.1"

import logging

from logtron_aws.cloudwatch import CloudWatchHandler
from logtron_aws.context import discover_context
from logtron import autodiscover as autodiscover_base


def autodiscover(name=None, level=logging.INFO, config=None, refresh=False, discover_context=discover_context):
    if config is not None:
        config = config.copy()
    else:
        config = {}

    if "handlers" not in config:
        config.update(
            {
                "handlers": ["logtron_aws.cloudwatch.CloudWatchHandler"],
            }
        )
    return autodiscover_base(name=name, level=level, config=config, refresh=refresh, discover_context=discover_context)
