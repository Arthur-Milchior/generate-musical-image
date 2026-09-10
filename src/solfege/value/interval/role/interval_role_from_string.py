

from dataclasses import dataclass
from typing import Dict, List, Tuple

from solfege.value.interval.role.interval_role import IntervalRole
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalRoleFromString(IntervalRole):
    """An `IntervalRole` whose guitar-image label is an arbitrary, explicitly given string (as opposed
    to `IntervalRoleFromInterval`, which derives it from the interval's own degree/alteration)."""
    role: str
    """The literal text to display for this role."""

    #pragma mark - IntervalRole
    def text_for_guitar_image(self) -> str:
        """Return `role` verbatim."""
        return self.role

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Dict:
        """No defaults of its own; delegates to the superclass chain."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        #kwargs["key"] = value
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Map a single positional argument to the `role` keyword argument."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "str")
        return args, kwargs

    def __post_init__(self) -> None:
        """Validate that `role` is a `str`."""
        assert_typing(self.role, str)
        super().__post_init__()

blue_role = IntervalRoleFromString("b")
"""Shared role instance used to mark the "blue note" (e.g. the flat fifth/tritone in a blues scale)."""

def role_from_interval_index(i: int) -> IntervalRoleFromString:
    """Build a role labelled with the plain 0-based index `i`, used for scale degrees that don't have
    a more specific role."""
    assert_typing(i, int)
    return IntervalRoleFromString(str(i))