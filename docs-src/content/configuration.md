---
title: Configuration
---

<!-- Logtron-AWS can be configured in a number of different ways:

- Through explicit configuration in code
- Through a YAML configuration file
- Through environment variables

These configs will get merged together as it searches for them in the following order (later configs merge into earlier configs, overriding keys on conflict):

1. YAML configuration file
2. Environment variables
3. Explicit configuration in code

## Logtron configuration

Logtron accepts an optional configuration dictionary that allows you to specify your own logging handlers based on python's `logging.Handler` base class.

This is a dict-like configuration that looks like this:

```python
{
    "handlers": [
        "logtron.handlers.ConsoleHandler",
        "my_lib.handlers.MyCustomHandler1",
        "my_other_lib.handlers.MyCustomHandler2",
        "my_other_other_lib.handlers.MyCustomHandler3",
    ],
    "my_lib.handlers.MyCustomHandler1": {
      "param1": 123,
      "param2": "abc",
    },
    "MyCustomHandler2": {
      "foo": "bar",
    },
}

```

- The `handlers` key specifies a list of full module path names to the handlers that you would like Logtron to use. If not specified, it will default to the internal `logtron.handlers.ConsoleHandler`.
- The `my_lib.handlers.MyCustomHandler1` key in this example is an optional way to specify additional parameters that will be passed into the constructor for this logging handler. This is using the full module path to the class.
- If there are no class naming conflicts, you can just specify only the name of the handler class itself as the key, as in the `MyCustomHandler2` example.

## Parameters

The full signature for the `autodiscover` function is:

```python
logger = logtron.autodiscover(
  name=None,
  level=logging.INFO,
  **kwargs,
)
```

| Parameter | Description                                                                   |
| --------- | ----------------------------------------------------------------------------- |
| `name`    | The name of the logger. This works exactly as with `logging.getLogger(name)`. |
| `level`   | The log level as defined in the `logging` package.                            |

The accepted keyword arguments are:

| Parameter          | Description                                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `flatten`          | If `True`, Logtron will flatten the JSON logs so that nested entries like `extra` and `context` are flattened to top level JSON keys. |
| `refresh`          | Forces re-initialization if set to `True`. Logtron will only initialize the first time `autodiscover` is called by default.           |
| `config`           | Explicit Logtron configuration.                                                                                                       |
| `discover_config`  | Function to override the default configuration discovery process.                                                                     |
| `discover_context` | Function to override the default context discovery process.                                                                           |

## Configuration File

Logtron will look for a `logtron.yaml` file in the current directory and try to parse it as a Logtron configuration. Here is a sample config file:

```yaml
handlers:
  - logtron.handlers.ConsoleHandler

logtron.handlers.ConsoleHandler:
  test_setting: 14
  test_float: 13.33
  test_str: foo
```

## Environment Variables

Logtron accepts all configuration entries as environment variables too. It looks for environment variables with a prefix of `LOGTRON` and splits on underscores to construct the configuration dictionary. If you have a list of items you would like to pass to a configuration entry, you can separate it with a comma and it will get interpreted as a list. Here's a sample usage:

```shell
$ LOGTRON_MYHANDLER_FOO=bar,baz python my_logging_app.py
``` -->
