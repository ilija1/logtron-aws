import logging

from importlib_metadata import version
from logtron import autodiscover as autodiscover_base

from logtron_aws.cloudwatch import CloudWatchHandler

try:
    __version__ = version(__package__)
except:
    __version__ = "unspecified"


def autodiscover(name=None, level=logging.INFO, **kwargs):
    config = kwargs.get("config")
    refresh = kwargs.get("refresh", False)
    logs_client = kwargs.get("logs_client")
    sts_client = kwargs.get("sts_client")
    discover_context = kwargs.get("discover_context")

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

    if logs_client is not None:
        config.update(
            {
                "CloudWatchHandler": {"logs_client": logs_client},
            }
        )

    if discover_context is None:
        from logtron_aws.context import discover_context as discover_context_base

        def __discover_context():
            return discover_context_base(sts_client)

        discover_context = __discover_context

    return autodiscover_base(name=name, level=level, config=config, refresh=refresh, discover_context=discover_context)


from logtron_aws.context import discover_context
