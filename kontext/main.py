from __future__ import annotations

from collections import UserDict
from contextvars import ContextVar
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar, Union, overload

from typing_extensions import Awaitable, ParamSpec, Protocol

R = TypeVar("R")
P = ParamSpec("P")
CT = TypeVar("CT")


class ContextDataProtocol(Protocol):  # pragma: no cover
    def copy(self) -> "ContextDataProtocol":
        ...

    def update(self, other: "ContextDataProtocol") -> None:
        ...

    def __setitem__(self, key: Any, item: Any) -> None:
        ...

    def __getitem__(self, key: Any) -> Any:
        ...


class ContextData(UserDict):  # type: ignore
    pass


_context: ContextVar[ContextDataProtocol] = ContextVar("__context__")


class ContextFactory(type):
    def __new__(
        cls,
        name: str,
        bases: Tuple[Any],
        attrs: Dict[str, Any],
        kontext: Optional[ContextVar[ContextDataProtocol]],
        default_cls: Optional[Type[ContextDataProtocol]],
    ) -> Any:
        return super().__new__(
            cls,
            name,
            bases,
            {
                **attrs,
                "_kontext": kontext or _context,
                "_default_cls": default_cls or ContextData,
            },
        )


class ContextMeta:  # pragma: no cover
    @property
    def _kontext(self) -> ContextVar[ContextDataProtocol]:
        raise NotImplementedError

    @property
    def _default_cls(self) -> Type[ContextDataProtocol]:
        raise NotImplementedError


class AbstractContext(ContextMeta):
    def __enter__(self) -> None:
        data = _get_or_default(self._kontext, self._default_cls)
        new_data = data.copy()
        new_data.update(data)
        self._token = self._kontext.set(new_data)

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        traceback: Any,
    ) -> None:
        self._kontext.reset(self._token)


class Context(
    AbstractContext,
    metaclass=ContextFactory,
    kontext=_context,
    default_cls=ContextData,
):
    @overload
    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        ...  # pragma: no cover

    @overload
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        ...  # pragma: no cover

    def __call__(
        self, func: Callable[P, R]
    ) -> Union[Callable[P, Awaitable[R]], Callable[P, R]]:
        if iscoroutinefunction(func):

            @wraps(func)
            async def async_inner(*args: P.args, **kwargs: P.kwargs) -> R:
                with Context():
                    return await func(*args, **kwargs)  # type: ignore

            return async_inner

        @wraps(func)
        def sync_inner(*args: P.args, **kwargs: P.kwargs) -> R:
            with Context():
                return func(*args, **kwargs)

        return sync_inner


class ContextProxyProtocol(Protocol):  # pragma: no cover
    def __setitem__(self, key: Any, item: Any) -> None:
        ...

    def __getitem__(self, key: Any) -> Any:
        ...

    def __repr__(self) -> str:
        ...

    def copy(self) -> ContextDataProtocol:
        ...


class AbstractContextProxy(ContextMeta):
    def __setitem__(self, key: Any, item: Any) -> None:
        data = _get_or_default(self._kontext, self._default_cls)
        data[key] = item

    def __getitem__(self, key: Any) -> Any:
        data = _get_or_default(self._kontext, self._default_cls)
        return data[key]

    def __repr__(self) -> str:
        data = _get_or_default(self._kontext, self._default_cls)
        return data.__repr__()

    def copy(self) -> ContextDataProtocol:
        data = _get_or_default(self._kontext, self._default_cls)
        return data.copy()


class ContextProxy(
    AbstractContextProxy,
    metaclass=ContextFactory,
    kontext=_context,
    default_cls=ContextData,
):
    pass


current_context = ContextProxy()


def _get_or_default(kontext: ContextVar[CT], default_cls: Type[CT]) -> CT:
    try:
        return kontext.get()
    except LookupError:
        data = default_cls()
        kontext.set(data)
        return data
