from typing import Any, Dict, Optional


class TooBigAlterationException(Exception):
    """Raised when a note/interval's alteration (distance from its "natural" diatonic value) is too
    large to be represented by any known `Alteration` subclass (e.g. more than a double sharp/flat).
    Carries a free-form `dic` of extra context, populated by callers via `__setitem__` as the
    exception propagates (e.g. `Pair.get_alteration` adds "The note which is too big")."""
    value: int
    """The offending (too large) alteration amount."""
    dic: Dict
    """Extra debugging context, keyed by a short description string."""

    def __init__(self, value: int, dic: Optional[Dict] = None) -> None:
        """`value` is the offending (too large) alteration amount; `dic` seeds the context dict."""
        self.value = value
        self.dic = dic or dict()
        super().__init__()

    def __repr__(self) -> str:
        """Debug representation including the offending value and context dict."""
        return f"""TooBigAlteration(value={self.value}, dic={self.dic})"""

    def __str__(self) -> str:
        """Same as `__repr__`."""
        return repr(self)

    def __getitem__(self, item: str) -> Optional[Any]:
        """Read a context value by key, or `None` if absent."""
        return self.dic.get(item)

    def __setitem__(self, key: str, value: Any) -> None:
        """Attach a context value under `key`, so callers can enrich the exception as it propagates."""
        self.dic[key] = value
