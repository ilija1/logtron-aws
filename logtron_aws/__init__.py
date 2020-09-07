from importlib_metadata import version

from logtron_aws.autodiscover import autodiscover
from logtron_aws.cloudwatch import CloudWatchHandler
from logtron_aws.context import discover_context

try:
    __version__ = version(__package__)
except:
    __version__ = "unspecified"
