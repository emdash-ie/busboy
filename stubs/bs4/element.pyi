from typing import Any, Callable, Dict, List, Optional, Union

from bs4 import ResultSet

class Tag(object):
    Filter = Union[str, List[str], Callable[[str], bool]]
    def __getitem__(self, index: str) -> Union[str, List[str]]: ...
    def __getattribute__(self, tag: str) -> Any: ...
    def find_all(
        self,
        name: Optional[Filter] = None,
        attrs: Dict[str, Filter] = {},
        recursive: bool = True,
        **kwargs: Any
    ) -> ResultSet: ...
