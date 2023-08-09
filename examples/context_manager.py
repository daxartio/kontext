import logging

from kontext import Context, current_context, setup_log_record

logging.basicConfig(format="%(message)s %(kontext)s", level=logging.INFO)
logger = logging.getLogger(__name__)


setup_log_record()

current_context["main"] = "..."
with Context():
    current_context["context_manager"] = "..."
    logger.info("context_manager")
logger.info("after context_manager")

# context_manager {'main': '...', 'context_manager': '...'}
# after context_manager {'main': '...'}
