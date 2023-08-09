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
