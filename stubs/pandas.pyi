from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Union

from numpy import ndarray

class DataFrame(object):
    def __getitem__(self, index: str) -> Any: ...
    def __setitem__(self, index: str, value: Any) -> None: ...
    def __init__(
        self, data: Union[ndarray, DataFrame, Dict[str, Any], None] = None
    ) -> None: ...
    def copy(self) -> DataFrame: ...
    def itertuples(self) -> Iterable[Any]: ...
    def set_index(self, keys: Union[str, List[str]]) -> DataFrame: ...
    def to_csv(
        self,
        filepath_or_buffer: Optional[str] = None,
        mode: str = "w",
        header: Union[bool, List[str]] = True,
        index: bool = True,
    ) -> Optional[str]: ...
    def fillna(self, value: Any = None) -> DataFrame: ...
    def notna(self) -> Any: ...
    loc: Any
    index: Any
    columns: Any

def concat(dfs: List[DataFrame]) -> DataFrame: ...
def read_csv(filepath_or_buffer: str) -> DataFrame: ...

NaN: float
NaT: datetime

class Series(object):
    def __getitem__(self, index: int) -> Any: ...
