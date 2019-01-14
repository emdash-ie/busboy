import typing as t

class cursor:
    def __enter__(self, *args: t.Any) -> cursor: ...
    def __exit__(self, *args: t.Any) -> None: ...
    def mogrify(self, query: t.Union[str, bytes], items: t.Tuple[t.Any, ...]) -> bytes: ...
    def execute(self, query: t.Union[str, bytes], values: t.List[t.Any] = ...) -> None: ...
    def fetchall(self) -> t.Iterable[t.Tuple[t.Any, ...]]: ...
_cursor = cursor
class connection:
    def __enter__(self, *args: t.Any) -> connection: ...
    def __exit__(self, *args: t.Any) -> None: ...
    def close(self) -> None: ...
    def cursor(self) -> _cursor: ...
