
        
from dataclasses import dataclass
from typing import Dict, List
from solfege.value.interval.interval import Interval
from solfege.value.interval.role.interval_role import IntervalRole
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalRoleFromInterval(IntervalRole):
    interval: Interval

    # Pragma mark - IntervalRole
    def text_for_guitar_image(self) -> str:
        return f"{self.interval._diatonic.value}{self.interval.get_alteration().letter()}"

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "interval")
        return args, kwargs

    def __post_init__(self):
        assert_typing(self.interval, Interval)
        super().__post_init__()