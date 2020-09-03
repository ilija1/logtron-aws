import logging
from importlib_metadata import version

from logtron_aws.cloudwatch import CloudWatchHandler
from logtron import autodiscover as autodiscover_base

try:
    __version__ = version(__package__)
except:
    pass


def autodiscover(
    name=None,
    level=logging.INFO,
    config=None,
    refresh=False,
    logs_client=None,
    sts_client=None,
    discover_context=None,
):
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
                "logtron_aws.cloudwatch.CloudWatchHandler": {"logs_client": logs_client},
            }
        )

    if discover_context is None:
        from logtron_aws.context import discover_context as discover_context_base

        def __discover_context():
            return discover_context_base(sts_client)

        discover_context = __discover_context

    return autodiscover_base(name=name, level=level, config=config, refresh=refresh, discover_context=discover_context)


from logtron_aws.context import discover_context
