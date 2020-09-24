---
title: API Reference
---

## `logtron_aws` Module

### `autodiscover`

```python
def autodiscover(
  name=None,
  level=logging.INFO,
  **kwargs,
):
...
```

**Returns:**

- A python `logging.Logger` instance configured for JSON logging.

**Parameters:**

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

---

<!-- ## `logtron.config` Module

### `discover_config`

```python
def discover_config(existing=None):
...
```

**Returns:**

- A merged dict-like configuration combined from the config discovery process. The order in which it is merged is:
  1. YAML configuration file
  2. Environment variables
  3. Explicit configuration in code

**Parameters:**

| Parameter  | Description                                                        |
| ---------- | ------------------------------------------------------------------ |
| `existing` | An existing dict-like config to merge into the discovered configs. |

---

## `logtron.formatters` Module

### `JsonFormatter`

```python
from logging import Formatter

class JsonFormatter(Formatter):
    def __init__(self, **kwargs):
      ...
```

**Returns:**

- A `logging.Formatter` which is capable of producing JSON log output.

**Parameters:**

The accepted keyword arguments for the constructor are:

| Parameter          | Description                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `flatten`          | If `True`, the formatter will flatten the JSON logs so that nested entries like `extra` and `context` are flattened to top level JSON keys. |
| `discover_context` | A custom function to use to discover the dict-like logging context which will be added to each log entry.                                   |

---

## `logtron.handlers` Module

### `ConsoleHandler`

```python
from logging import StreamHandler

class ConsoleHandler(StreamHandler):
    def __init__(self, **kwargs):
      ...
```

**Returns:**

- A `logging.StreamHandler` which will log to the console.

---

## `logtron.util` Module

### `merge`

```python
def merge(d, u):
  ...
```

**Returns:**

- A deep-merged dict based on the `d` parameter with `u` merged into it. This will update the `d` parameter directly as well as returning it.

**Parameters:**

The accepted keyword arguments for the constructor are:

| Parameter | Description                    |
| --------- | ------------------------------ |
| `d`       | A dict-like to merge `u` into. |
| `u`       | A dict-like to merge into `d`. |

---

### `flatten_dict`

```python
def flatten_dict(d, parent_key="", sep="_"):
  ...
```

**Returns:**

- A flattened dict based on the `d` parameter. This will pull up all nested keys to the top level in the dict and give them names based on the separator, i.e.

  ```python
  my_dict = {
    'level1': {
      'level2': {
        'foo': 'bar'
      }
    }
  }

  # becomes

  my_dict['level1_level2_foo'] = 'bar'
  ```

**Parameters:**

The accepted keyword arguments for the constructor are:

| Parameter    | Description                                |
| ------------ | ------------------------------------------ |
| `d`          | A dict-like to flatten.                    |
| `parent_key` | An optional prefix for the flattened keys. |
| `sep`        | The separator to use when flattening.      |

---

### `parse_env`

```python
def parse_env(prefix=None, env=os.environ):
  ...
```

**Returns:**

- A dict representing parsed environment variables. This will split the env var names on `_` and create a deeply nested dict using them.

**Parameters:**

The accepted keyword arguments for the constructor are:

| Parameter | Description                                                         |
| --------- | ------------------------------------------------------------------- |
| `prefix`  | An optional prefix to use when searching the environment variables. |
| `env`     | An optional explicit dict-like of environment variables to use.     | -->
