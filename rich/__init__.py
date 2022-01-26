import os
from typing import (
    Any,
    Callable,
    IO,
    NoReturn,
    Optional,
    TYPE_CHECKING,
)

from ._extension import load_ipython_extension

if TYPE_CHECKING:
    from .console import Console

__all__ = ["get_console", "reconfigure", "print", "inspect"]

_console: Optional["Console"] = None

_IMPORT_CWD = os.path.abspath(os.getcwd())


def get_console() -> "Console":
    global _console
    if _console is None:
        from .console import Console

        _console = Console()

    return _console


def reconfigure(*args: Any, **kwargs: Any) -> NoReturn:
    global _console
    from rich.console import Console

    new_console = Console(*args, **kwargs)
    _console = get_console()
    _console.__dict__ = new_console.__dict__


# noinspection PyShadowingBuiltins
def print(
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        file: Optional[IO[str]] = None,
        flush: bool = True,
) -> NoReturn:
    from .console import Console
    if not flush:
        raise Warning("Console 是总是刷新的")
    write_console = get_console() if file is None else Console(file=file)
    return write_console.print(*objects, sep=sep, end=end)


def print_json(
        json: Optional[str] = None,
        *,
        data: Any = None,
        indent: int = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        default: Optional[Callable[[Any], Any]] = None,
        sort_keys: bool = False,
) -> NoReturn:
    get_console().print_json(
        json,
        data=data,
        indent=indent,
        highlight=highlight,
        skip_keys=skip_keys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        default=default,
        sort_keys=sort_keys,
    )


# noinspection PyShadowingNames,PyShadowingBuiltins
def inspect(
        obj: Any,
        *,
        console: Optional["Console"] = None,
        title: Optional[str] = None,
        help: bool = False,
        methods: bool = False,
        docs: bool = True,
        private: bool = False,
        dunder: bool = False,
        sort: bool = True,
        all: bool = False,
        value: bool = True,
) -> NoReturn:
    global _console
    _console = console or get_console()
    from rich._inspect import Inspect

    is_inspect = obj is inspect

    _inspect = Inspect(
        obj,
        title=title,
        help=is_inspect or help,
        methods=is_inspect or methods,
        docs=is_inspect or docs,
        private=private,
        dunder=dunder,
        sort=sort,
        all=all,
        value=value,
    )
    _console.print(_inspect)


if __name__ == "__main__":  # pragma: no cover
    print("Hello, **World**")
