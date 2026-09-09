
        
from dataclasses import dataclass
from typing import Dict, List
from solfege.value.interval.interval import Interval
from solfege.value.interval.role.interval_role import IntervalRole
from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalRoleFromInterval(IntervalRole):
    """Default `IntervalRole` derived straight from the interval itself (its diatonic degree number
    plus alteration letter, e.g. "3M"), used when no explicit role/name was set — see
    `Interval.get_role`."""
    interval: Interval
    """The interval this role is derived from."""

    # Pragma mark - IntervalRole
    def text_for_guitar_image(self) -> str:
        """The interval's 1-based diatonic degree followed by its alteration letter (e.g. "3M"), or
        "?" for the alteration part if it's too large to name."""
        try:
            alteration = self.interval.get_alteration().letter()
        except TooBigAlterationException:
            alteration = "?"
        return f"{self.interval._diatonic.value + 1}{alteration}"

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """No defaults of its own; delegates to the superclass chain."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Map a single positional argument to the `interval` keyword argument."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval")
        return args, kwargs

    def __post_init__(self):
        """Validate that `interval` is an `Interval`."""
        assert_typing(self.interval, Interval)
        super().__post_init__()