from contextvars import ContextVar
from threading import Thread

import pytest

from kontext.main import (
    AbstractContext,
    AbstractContextProxy,
    Context,
    ContextDataProtocol,
    ContextFactory,
    current_context,
)

var: ContextVar[ContextDataProtocol] = ContextVar("var")


def test_context_repr():
    with Context():
        current_context["key"] = "value"
        assert repr(current_context) == "{'key': 'value'}"


def test_context_decorator():
    @Context()
    def fn():
        current_context["key"] = "value"

        assert current_context["key"] == "value"

    fn()

    with pytest.raises(KeyError):
        _ = current_context["key"]


def test_context_with():
    with Context():
        current_context["key"] = "value"
        assert current_context["key"] == "value"

    with pytest.raises(KeyError):
        _ = current_context["key"]


def test_context_inner():
    with Context():
        current_context["key"] = "value"

        with Context():
            assert current_context["key"] == "value"
            current_context["key"] = "value2"
            assert current_context["key"] == "value2"

            current_context["key2"] = "value"
            assert current_context["key2"] == "value"

        assert current_context["key"] == "value"

        with pytest.raises(KeyError):
            _ = current_context["key2"]


def test_context_thread():
    def fn():
        current_context["key"] = "value"
        assert current_context["key"] == "value"

    thread = Thread(target=fn)
    thread.start()
    thread.join()

    with pytest.raises(KeyError):
        _ = current_context["key"]


@pytest.mark.asyncio()
async def test_context_async():
    @Context()
    async def fn():
        current_context["key"] = "value"

        assert current_context["key"] == "value"

    await fn()

    with pytest.raises(KeyError):
        _ = current_context["key"]


def test_custom_context():
    class CustomContext(
        AbstractContext,
        metaclass=ContextFactory,
        default_cls=dict,
        kontext=var,
    ):
        pass

    class CustomContextProxy(
        AbstractContextProxy,
        metaclass=ContextFactory,
        default_cls=dict,
        kontext=var,
    ):
        pass

    custom_current_context = CustomContextProxy()

    with CustomContext():
        custom_current_context["key"] = "value"
        assert custom_current_context["key"] == "value"

        with pytest.raises(KeyError):
            _ = current_context["key"]


def test_context_update():
    current_context["key"] = "origin"

    with Context():
        current_context["key"] = "value"
        current_context.update(key="value2", foo="bar")
        assert current_context["key"] == "value2"
        assert current_context["foo"] == "bar"

    assert current_context["key"] == "origin"
