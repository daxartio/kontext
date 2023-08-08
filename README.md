# Python Context Information

[![PyPI](https://img.shields.io/pypi/v/ctx)](https://pypi.org/project/ctx/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ctx)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/ctx)](https://github.com/daxartio/ctx)
[![GitHub stars](https://img.shields.io/github/stars/daxartio/ctx?style=social)](https://github.com/daxartio/ctx)

The plugin allows to transfer a context between functions. Inspired by [context-logging](https://github.com/Afonasev/context_logging).

You can use it for logging data which does not change and can be correlated, e.g. `trace_id`, `correlation_id` etc.

## Installation

```
pip install ctx
```

## Usage

```python
import logging

from ctx import Context, current_context, setup_log_record

logging.basicConfig(format="%(message)s %(ctx)s", level=logging.INFO)
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
# foo {'key': 'value'}
# bar {'key': 'value', 'foo': 'bar'}

```

## License

* [MIT LICENSE](LICENSE)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
