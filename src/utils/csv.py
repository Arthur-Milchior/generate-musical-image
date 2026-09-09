from abc import ABC, abstractmethod
from typing import Generator, List

from utils.util import assert_typing


class CsvGenerator(ABC):
    """Mixin for objects that can render themselves as one CSV row."""

    def csv(self, *args, **kwargs)->str:
        """Return `self` as one double-quoted, comma-separated CSV row, built from `csv_content(*args, **kwargs)`.
        Asserts each field is a `str` containing no `"` (fields are not escaped, just wrapped in quotes)."""
        csv_content = list(self.csv_content(*args, **kwargs))
        for content in csv_content:
            assert_typing(content, str)
            assert '"' not in content
        return ",".join(f'"{content}"' for content in csv_content)

    #Must be implemented by subclasses
    @abstractmethod
    def csv_content(self) -> Generator[str]:
        """Yield the raw (unquoted) field values that make up this object's CSV row, in order."""