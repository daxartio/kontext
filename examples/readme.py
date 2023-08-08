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
