import logging

import pytest

from kontext.log_record import _SETUP_DONE, setup_log_record

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def _clear_log_record_factory():
    old_factory = logging.getLogRecordFactory()
    yield
    logging.setLogRecordFactory(old_factory)
    _SETUP_DONE.clear()


def test_setup_log_record(caplog):
    setup_log_record()

    logger.info("test")

    assert "test" in caplog.text


def test_setup_log_record_twice(mocker):
    old_facatory = logging.getLogRecordFactory()
    record_factory = mocker.patch("kontext.log_record.record_factory", autospec=True)
    record_factory.return_value = lambda *args, **kwargs: old_facatory(*args, **kwargs)

    setup_log_record()
    setup_log_record()

    assert record_factory.call_count == 1
