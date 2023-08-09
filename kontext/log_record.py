import logging
from typing import Any, Callable

from .main import ContextProxyProtocol, current_context


def record_factory(
    old_factory: Callable[..., logging.LogRecord],
    context: ContextProxyProtocol,
) -> Callable[..., logging.LogRecord]:
    def create_record(*args: Any, **kwargs: Any) -> logging.LogRecord:
        record = old_factory(*args, **kwargs)
        record.kontext = context.copy()
        return record

    return create_record


def setup_log_record() -> None:
    logging.setLogRecordFactory(
        record_factory(
            logging.getLogRecordFactory(),
            current_context,
        )
    )
