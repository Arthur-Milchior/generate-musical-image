from typing import Dict, Optional


class TooBigAlterationException(Exception):
    dic: Dict

    def __init__(self, value: int, dic: Optional[Dict] = None):
        self.value = value
        self.dic = dic or dict()
        super().__init__()

    def __repr__(self):
        return f"""TooBigAlteration(value={self.value}, dic={self.dic})"""

    def __getitem__(self, item):
        return self.dic.get(item)

    def __setitem__(self, key, value):
        self.dic[key] = value
