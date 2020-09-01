# Logtron-AWS

[![Release](https://img.shields.io/pypi/v/logtron-aws?logo=python&style=flat)](https://pypi.org/project/logtron-aws)
[![Downloads](https://img.shields.io/pypi/dm/logtron-aws?logo=python&style=flat)](https://pypi.org/project/logtron-aws)
[![Supported Versions](https://img.shields.io/pypi/pyversions/logtron-aws.svg?logo=python&style=flat)](https://pypi.org/project/logtron-aws)
[![License](https://img.shields.io/github/license/ilija1/logtron-aws?logo=apache&style=flat)](LICENSE)

[![Build](https://img.shields.io/travis/ilija1/logtron-aws?logo=travis&style=flat)](https://travis-ci.org/ilija1/logtron-aws)
[![Coverage](https://img.shields.io/codecov/c/gh/ilija1/logtron-aws?logo=codecov&style=flat)](https://codecov.io/gh/ilija1/logtron-aws)
[![Documentation](https://img.shields.io/readthedocs/logtron-aws?logo=read-the-docs&style=flat)](https://logtron-aws.readthedocs.io/en/latest)
[![Maintainability](https://img.shields.io/codeclimate/maintainability/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/maintainability)
[![Tech Debt](https://img.shields.io/codeclimate/tech-debt/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/issues)
[![Issues](https://img.shields.io/codeclimate/issues/ilija1/logtron-aws?logo=code-climate&style=flat)](https://codeclimate.com/github/ilija1/logtron-aws/issues)

**Logtron-AWS** is a set of AWS-targeted extensions for the [**Logtron**](https://github.com/ilija1/logtron) library.

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

Logtron-AWS provides a set of extensions for the [Logtron](https://github.com/ilija1/logtron) library to enable features such as:

- Automated log context discovery using AWS STS
- Log handler for logging directly to CloudWatch Logs
  - Automatic log group creation
  - Convention-based log group naming derived from IAM role name
  - Configurable log retention period
  - Automated background log batch submission to support high frequency logging
  - Configureable batch submission time interval
- Highly configurable if needed, but has sane defaults out-of-the-box

## Installing Logtron-AWS and Supported Versions

Logtron-AWS is available on PyPI:

```shell
$ python -m pip install logtron-aws
```

Logtron-AWS officially supports Python 2.7 & 3.5+.
