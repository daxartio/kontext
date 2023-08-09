import logging
from threading import Thread, current_thread

from kontext import current_context, setup_log_record

logging.basicConfig(format="%(message)s %(kontext)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def bar(a=0, b=None):
    current_context["a"] = a
    if b:
        current_context["b"] = b
    logger.info("Bar %s", current_thread().name)


if __name__ == "__main__":
    setup_log_record()
    bar(1)
    logger.info("Start")
    t = Thread(target=bar, args=(2, "..."))
    t.start()
    t.join()
    logger.info("Finish")

# Bar MainThread {'a': 1}
# Start {'a': 1}
# Bar Thread-1 {'a': 2, 'b': '...'}
# Finish {'a': 1}
