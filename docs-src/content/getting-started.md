---
title: Getting started
---

## Installation

Logtron-AWS is available on PyPI:

```shell
$ python -m pip install logtron-aws
```

## Usage

```python
import logtron_aws as logtron

logger = logtron.autodiscover()

# Now we're ready to use the logger
logger.info("This is a test", extra={"var1": "1234"})
# {"timestamp": 1600574833223, "message": "This is a test", "name": "root", "level": 20, "extra": {"var1": "1234"}, "context": {}}

# We're able to capture exception details as well
try:
  num = 1 / 0
except:
  logger.error("An error occurred.", exc_info=True, extra={"my": "information", "number": 123})
# {"timestamp": 1600574833224, "message": "An error occurred.", "name": "root", "level": 40, "exception": "Traceback (most recent call last):\n  File \"<stdin>\", line 2, in <module>\nZeroDivisionError: division by zero\n", "extra": {"my": "information", "number": 123}, "context": {}}

# We can create other loggers as well, logtron will configure the python root logger by default
import logging

my_logger = logging.getLogger("my_context")
my_logger.info("Hello World")
# {"timestamp": 1600574834158, "message": "Hello World", "name": "my_context", "level": 20, "extra": {}, "context": {}}

```

## Configuration

Logtron-AWS comes with sane defaults out of the box, but is highly configurable. Check out the [configuration docs](/content/configuration) for more information.
