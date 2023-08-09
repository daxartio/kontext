import logging

from kontext.log_record import setup_log_record

logger = logging.getLogger(__name__)


def test_log_record(caplog):
    setup_log_record()

    logger.info("test")

    assert "test" in caplog.text
