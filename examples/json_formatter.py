import json
import logging
import logging.config

from kontext import Context, current_context


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa
        data = {
            "message": record.getMessage(),
        }

        try:
            data["ctx"] = current_context.copy().__dict__["data"]
        except Exception:  # noqa
            data["ctx"] = str(current_context.copy())

        return json.dumps(data)


logging.basicConfig(format="%(message)s", level=logging.INFO)
logging.root.handlers[0].setFormatter(JsonFormatter())
logger = logging.getLogger(__name__)


current_context["app_name"] = "..."
with Context():
    current_context["request_id"] = "123"
    logger.info("context_manager")

logger.info("after context_manager")
