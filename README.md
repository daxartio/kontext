# Python Context Information

[![PyPI](https://img.shields.io/pypi/v/kontext)](https://pypi.org/project/kontext/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kontext)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/kontext)](https://github.com/daxartio/kontext)
[![GitHub stars](https://img.shields.io/github/stars/daxartio/kontext?style=social)](https://github.com/daxartio/kontext)

The plugin allows to transfer a context between functions. Inspired by [context-logging](https://github.com/Afonasev/context_logging).

You can use it for logging data which does not change and can be correlated, e.g. `trace_id`, `correlation_id` etc.

## Features

- Thread-safe context management
- Customizable log records
- Easy-to-use API

## Installation

```
pip install kontext
```

## Usage

```python
import logging

from kontext import Context, current_context, setup_log_record

logging.basicConfig(format="%(message)s %(kontext)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def bar():
    current_context["foo"] = "bar"
    logger.info("bar")


@Context()
def foo():
    current_context["key"] = "value"
    logger.info("foo")
    bar()


setup_log_record()
foo()
logger.info("Finish")
# foo {'key': 'value'}
# bar {'key': 'value', 'foo': 'bar'}
# Finish {}

```

For more examples, please refer to the examples directory.

## License

* [MIT LICENSE](LICENSE)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
