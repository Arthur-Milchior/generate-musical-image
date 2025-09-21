from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import math
from typing import Dict, List, Optional, TypeVar

from solfege.value.abstract import Abstract
from solfege.value.interval.role.interval_role import IntervalRole
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True, eq=False, repr=False)
class AbstractInterval(Abstract, ABC):
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be set, because the object is supposed to be immutable.

    Inheriting class which are instantiated should contain the following variable:
    * DiatonicClass: class to which a chromatic object must be converted when a diatonic object is required.
    * PairClass: the class to which a diatonic and chromatic object must be converted."""
    _role: Optional[IntervalRole] = field(hash=False, compare=False)
    
    def __neg__(self):
        return self * -1

    def get_role(self) -> IntervalRole:
        assert self._role is not None
        return self._role
    
    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["_role"] = None
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "_role")
        return args, kwargs

    def __post_init__(self):
        super().__post_init__()
    
    # must be implemented by subclasses
    
    @classmethod
    @abstractmethod
    def unison(cls):
        return NotImplemented


IntervalType = TypeVar('IntervalType', bound=AbstractInterval)