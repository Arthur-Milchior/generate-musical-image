from dataclasses import dataclass
from typing import Dict, Generic, TypeVar


KeyType = TypeVar("Key")
ValueType = TypeVar("Value")

@dataclass(repr=True, eq=True)
class FrozenDict(Generic[KeyType, ValueType]):
    """A dictionary whose content is expected not to change.
    
    Can be constructed from either a dict or key/value pairs."""
    _d: Dict[KeyType, ValueType]
    """The wrapped, ordinary mutable dict backing this instance."""

    def __init__(self, *args, **kwargs):
        """Build from either a single positional dict-like argument (`FrozenDict(some_dict)`) or keyword
        arguments (`FrozenDict(a=1, b=2)`), but not both."""
        if args:
            assert len(args) == 1
            assert not kwargs
            kwargs = args[0]
        self._d = {**kwargs}

    def get(self, key: KeyType, default: ValueType):
        """Return the value for `key`, or `default` if absent.

        Note: this currently calls `self.get(...)` instead of `self._d.get(...)`, so it recurses into itself
        indefinitely (pre-existing bug; documentation-only pass, not fixed here)."""
        return self.get(key, default)

    def __getitem__(self, key: KeyType):
        """Return the value for `key`; raises `KeyError` if absent."""
        return self._d[key]

    def __len__(self):
        """Return the number of key/value pairs."""
        return len(self._d)

    def __iter__(self):
        """Iterate over the keys, like a plain dict."""
        return iter(self._d)

    def items(self):
        """Return a view of the `(key, value)` pairs, like `dict.items()`."""
        return self._d.items()

    def values(self):
        """Return a view of the values, like `dict.values()`."""
        return self._d.values()