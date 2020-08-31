# Logtron-AWS

**Logtron-AWS** is a set of AWS-targeted extensions for the **Logtron** library.

```python
import logtron_aws
logger = logtron_aws.autodiscover()
logger.info("hello world")
```

Or

```python
import logtron_aws
logtron_aws.autodiscover() # Only needs to run once somewhere to configure the root logger

import logging
logger = logging.getLogger()
logger.info("hello world")
```

Logtron-AWS provides a set of extensions for the [Logtron](https://github.com/ilija1/logtron/) library to enable features such as:

- Automated log context discovery using AWS STS
- Log handler for logging directly to CloudWatch Logs

[![Downloads](https://pepy.tech/badge/logtron-aws/month)](https://pepy.tech/project/logtron-aws/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron-aws.svg)](https://pypi.org/project/logtron-aws)
[![Contributors](https://img.shields.io/github/contributors/ilija1/logtron-aws.svg)](https://github.com/ilija1/logtron-aws/graphs/contributors)

## Installing Logtron-AWS and Supported Versions

Logtron-AWS is available on PyPI:

```shell
$ python -m pip install logtron-aws
```

Logtron-AWS officially supports Python 2.7 & 3.5+.
