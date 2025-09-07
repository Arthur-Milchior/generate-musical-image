from typing import List


class CsvGenerator:
    def csv_content(self) -> List[str]:
        return NotImplemented
    
    def csv(self, *args, **kwargs)->str:
        csv_content = self.csv_content(*args, **kwargs)
        for content in csv_content:
            assert '"' not in content
        return ",".join(f'"{content}"' for content in csv_content)