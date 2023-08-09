"""Example.

Bar MainThread {'a': 1, 'b': 2, 'c': 3}
Bar MainThread {'a': 2, 'b': 3, 'c': 3}
Foo MainThread {'a': 1, 'b': 2, 'c': 3}
After foo {}
Bar Thread-1 {'b': 2, 'c': 3}
Bar MainThread {'b': 3, 'c': 3}
Finish {'b': 3, 'c': 3}
"""

import logging
from threading import Thread, current_thread

from kontext import Context, current_context, setup_log_record

logging.basicConfig(format="%(message)s %(kontext)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def bar():
    current_context["c"] = 3
    logger.info("Bar %s", current_thread().name)


def baz(c=0):
    current_context["b"] = 2 + c
    bar()


@Context()
def foo():
    current_context["a"] = 1
    baz()
    with Context():
        current_context["a"] = 2
        baz(1)
    logger.info("Foo %s", current_thread().name)


if __name__ == "__main__":
    setup_log_record()
    foo()
    logger.info("After foo")
    t = Thread(target=baz)
    t.start()
    t.join()
    baz(1)
    logger.info("Finish")
