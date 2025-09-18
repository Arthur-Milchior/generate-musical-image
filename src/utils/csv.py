from abc import ABC, abstractmethod
from typing import Generator, List

from utils.util import assert_typing


class CsvGenerator(ABC):
    def csv(self, *args, **kwargs)->str:
        csv_content = list(self.csv_content(*args, **kwargs))
        for content in csv_content:
            assert_typing(content, str)
            assert '"' not in content
        return ",".join(f'"{content}"' for content in csv_content)

    #Must be implemented by subclasses
    @abstractmethod
    def csv_content(self) -> Generator[str]:
        return NotImplemented