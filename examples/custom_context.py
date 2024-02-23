import logging
from contextvars import ContextVar

from kontext import (
    AbstractContext,
    AbstractContextProxy,
    ContextDataProtocol,
    ContextFactory,
)
from kontext.log_record import record_factory

logging.basicConfig(format="%(message)s %(kontext)s", level=logging.INFO)
logger = logging.getLogger(__name__)

_context: ContextVar[ContextDataProtocol] = ContextVar("var")


class CustomContext(
    AbstractContext,
    metaclass=ContextFactory,
    default_cls=dict,
    kontext=_context,
):
    pass


class CustomContextProxy(
    AbstractContextProxy,
    metaclass=ContextFactory,
    default_cls=dict,
    kontext=_context,
):
    pass


custom_context = CustomContextProxy()

logging.setLogRecordFactory(
    record_factory(logging.getLogRecordFactory(), custom_context)
)


with CustomContext():
    custom_context["key"] = "value"

    logger.info("Custom Context")

logger.info("Finish")
