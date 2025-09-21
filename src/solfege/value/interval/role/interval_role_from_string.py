

from dataclasses import dataclass
from typing import Dict, List

from solfege.value.interval.role.interval_role import IntervalRole
from utils.util import assert_typing


@dataclass(frozen=True)
class IntervalRoleFromString(IntervalRole):
    role: str

    #pragma mark - IntervalRole
    def text_for_guitar_image(self) -> str: 
        return self.role

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        #kwargs["key"] = value
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "str")
        return args, kwargs

    def __post_init__(self):
        assert_typing(self.role, str)
        super().__post_init__()

blue_role = IntervalRoleFromString("b")

def role_from_interval_index(i: int):
    assert_typing(i, int)
    return IntervalRoleFromString(str(i))