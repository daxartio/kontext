# Python Context Information

[![PyPI](https://img.shields.io/pypi/v/ctx)](https://pypi.org/project/ctx/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ctx)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/ctx)](https://github.com/daxartio/ctx)
[![GitHub stars](https://img.shields.io/github/stars/daxartio/ctx?style=social)](https://github.com/daxartio/ctx)

## Installation

```
pip install ctx
```

## Usage

```python
from ctx import Context, current_context, setup_log_record

@Context
def ctx():
    current_context["key"] = "value"

setup_log_record()
ctx()
```

## License

* [MIT LICENSE](LICENSE)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
