from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Self, TypeVar, ClassVar

from solfege.value.abstract import Abstract
from solfege.value.singleton import Singleton
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True, eq=False)
class AbstractInterval(Abstract):
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be set, because the object is supposed to be immutable.

    Inheriting class which are instantiated should contain the following variable:
    * DiatonicClass: class to which a chromatic object must be converted when a diatonic object is required.
    * PairClass: the class to which a diatonic and chromatic object must be converted."""
    
    @classmethod
    def unison(cls):
        return NotImplemented
    
    def __neg__(self):
        return self * -1

IntervalType = TypeVar('IntervalType', bound=AbstractInterval)