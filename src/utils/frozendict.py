from dataclasses import dataclass
from typing import Dict, Generic, TypeVar


KeyType = TypeVar("Key")
ValueType = TypeVar("Value")

@dataclass(repr=True, eq=True)
class FrozenDict(Generic[KeyType, ValueType]):
    """A dictionary whose content is expected not to change.
    
    Can be constructed from either a dict or key/value pairs."""
    _d: Dict[KeyType, ValueType]

    def __init__(self, *args, **kwargs):
        if args:
            assert len(args) == 1
            assert not kwargs
            kwargs = args[0]
        self._d = {**kwargs}

    def get(self, key: KeyType, default: ValueType):
        return self.get(key, default)

    def __getitem__(self, key: KeyType):
        return self._d[key]
    
    def __len__(self):
        return len(self._d)
    
    def __iter__(self):
        return iter(self._d)
    
    def items(self):
        return self._d.items()
    
    def values(self):
        return self._d.values()