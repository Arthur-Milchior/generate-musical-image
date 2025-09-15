from typing import List

from utils.util import assert_typing


class CsvGenerator:
    def csv(self, *args, **kwargs)->str:
        csv_content = self.csv_content(*args, **kwargs)
        for content in csv_content:
            assert_typing(content, str)
            assert '"' not in content
        return ",".join(f'"{content}"' for content in csv_content)

    #Must be implemented by subclasses
    def csv_content(self) -> List[str]:
        return NotImplemented