import logging

from logtron import autodiscover as autodiscover_base
from logtron.config import discover_config
from logtron.util import merge

from logtron_aws.context import discover_context as discover_context_base

DEFAULT_HANDLER_FULL_PATH = "logtron_aws.cloudwatch.CloudWatchHandler"
DEFAULT_HANDLER_CLASS = "CloudWatchHandler"

is_configured = False


def __has_emf(config):
    if len(config) == 0:
        return False
    handler_config = {}
    for i in [DEFAULT_HANDLER_FULL_PATH, DEFAULT_HANDLER_CLASS]:
        merge(handler_config, config.get(i, {}))
    emf_metrics = handler_config.get("emf_metrics", [])
    return len(emf_metrics) > 0


def autodiscover(name=None, level=logging.INFO, **kwargs):
    global is_configured

    refresh = kwargs.pop("refresh", False)
    if not refresh and is_configured:
        return logging.getLogger(name)

    logs_client = kwargs.pop("logs_client", None)
    sts_client = kwargs.pop("sts_client", None)
    config = kwargs.pop("config", {})
    discover_context = kwargs.pop("discover_context", None)
    flatten = kwargs.pop("flatten", __has_emf(config))

    if "handlers" not in config:
        use_threading = kwargs.pop("use_threading", True)
        merge(
            config,
            {
                "handlers": [DEFAULT_HANDLER_FULL_PATH],
                DEFAULT_HANDLER_CLASS: {"use_threading": use_threading},
            },
        )

    if logs_client is not None:
        merge(
            config,
            {
                DEFAULT_HANDLER_CLASS: {"logs_client": logs_client},
            },
        )

    if discover_context is None:
        discover_context = lambda: discover_context_base(sts_client=sts_client, refresh=refresh)

    is_configured = True

    return autodiscover_base(
        name=name,
        level=level,
        config=config,
        refresh=refresh,
        flatten=flatten,
        discover_context=discover_context,
        **kwargs
    )
