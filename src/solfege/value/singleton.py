from dataclasses import dataclass
import math
from typing import Callable, ClassVar, Dict, List, Self, Type, TypeVar, Union

from solfege.value.abstract import Abstract
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing


@dataclass(frozen=True, eq=False)
class Singleton(Abstract, MakeableWithSingleArgument):
    """Base for a value (note or interval) represented by a single int, i.e. `Chromatic` or `Diatonic`
    (as opposed to `Pair`, which needs both components). The int is a count of semitones or scale
    degrees, depending on the subclass."""
    # Must be implemented by subclasses.
    IntervalClass: ClassVar[Type[Self]]
    """The interval class matching this class (see `Abstract.IntervalClass`)."""

    number_of_interval_in_an_octave: ClassVar[int]
    """Number of steps per octave for this representation: 7 for diatonic, 12 for chromatic."""

    #public
    value: int
    """The raw count of semitones (chromatic) or scale degrees (diatonic), 0 at C4/unison."""

    @classmethod
    def make_instance_of_selfs_class(cls: Type[Self], value: int):
        """Build a new instance of `cls` from a raw int `value`."""
        return cls.make(value)

    def __post_init__(self):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used."""
        assert_typing(self.value, int)

    def __eq__(self, other):
        """Equal iff `other` is the exact same class and has the same `value`; raises if the classes
        differ, rather than silently returning False, to catch accidental cross-class comparisons
        (e.g. a `ChromaticNote` compared to a `ChromaticInterval`)."""
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self}:{self.__class__} and {other}:{other.__class__}")
        return self.value == other.value

    def __hash__(self):
        """Hash by the raw int value."""
        return self.value

    def __le__(self, other: Self):
        """Ordered by `value`; `other` must be the same class."""
        assert_typing(other, self.__class__)
        return self.value <= other.value

    def __lt__(self, other: Self):
        """Ordered by `value`; `other` must be the same class."""
        assert_typing(other, self.__class__)
        return self.value < other.value

    def __repr__(self):
        """Evaluable repr, e.g. `ChromaticNote(value=0)`."""
        return f"{self.__class__.__name__}(value={self.value})"

    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        """The raw int value, as text, used by `MakeableWithSingleArgument`."""
        return f"""{self.value}"""

    @classmethod
    def _make_single_argument(cls, value: int) -> Self:
        """Build an instance from a single int argument (the value)."""
        assert_typing(value, int)
        return cls.make_instance_of_selfs_class(value)
    
    #pragma mark - Abstract
    
    def octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.value / self.__class__.number_of_interval_in_an_octave)

    @classmethod
    def one_octave(cls) -> Self:
        """The value representing exactly one octave (i.e. `number_of_interval_in_an_octave` as a value)."""
        return cls.make_instance_of_selfs_class(value=cls.number_of_interval_in_an_octave)

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        """No defaults of its own; delegates to the superclass chain."""
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        return kwargs

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        """Map a single positional argument to the `value` keyword argument."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "value")
        return args, kwargs

    def __post_init__(self):
        """Delegates to the superclass chain (no extra validation of its own beyond `Abstract`'s)."""
        super().__post_init__()


SingletonType = TypeVar("SingletonType", bound=Singleton)