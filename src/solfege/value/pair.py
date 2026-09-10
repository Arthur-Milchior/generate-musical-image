from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, Generic, List, Self, Tuple, Type, Union

from solfege.value.abstract import Abstract
from solfege.value.chromatic import Chromatic, ChromaticGetter, ChromaticType
from solfege.value.diatonic import Diatonic, DiatonicGetter, DiatonicType
from solfege.value.interval.alteration.alteration import Alteration, AlterationType
from solfege.value.interval.alteration.wrong_alteration import WrongAlteration
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True)
class Pair(Abstract, MakeableWithSingleArgument, ChromaticGetter, DiatonicGetter, Generic[ChromaticType, DiatonicType, AlterationType]):
    """A value (note or interval) represented by both a chromatic (semitone) and a diatonic (scale-degree)
    component together, e.g. distinguishing G# from Ab even though they share the same chromatic value.
    `Note` and `Interval` are its concrete subclasses; built via `Pair.make(chromatic, diatonic)`, never
    the generated `__init__` directly."""
    DiatonicClass: ClassVar[Type[Diatonic]] = Diatonic
    """The diatonic-only class used to represent/build this pair's diatonic component."""
    ChromaticClass: ClassVar[Type[Chromatic]] = Chromatic
    """The chromatic-only class used to represent/build this pair's chromatic component."""
    IntervalClass: ClassVar[Type["Pair"]]
    """The interval `Pair` subclass matching this class (e.g. a note class points at its interval class)."""

    _chromatic: ChromaticType
    """The chromatic (semitone) component of this value."""
    _diatonic: DiatonicType
    """The diatonic (scale-degree) component of this value."""

    @classmethod
    def make_instance_of_selfs_class(cls: Type["Pair"], _chromatic: ChromaticType, _diatonic: DiatonicType) -> "Pair":
        """Build a new instance of `cls` from an explicit chromatic and diatonic component."""
        return cls.make(_chromatic, _diatonic)

    @classmethod
    def from_chromatic(cls, chromatic: ChromaticType) -> "Pair":
        """Return the `Pair` matching `chromatic`, spelled using the diatonic note that a major scale
        would use at that chromatic position (i.e. no sharps/flats: black keys are spelled as the
        diatonic note below them, e.g. C# is spelled using diatonic C). Use `all_from_chromatic` to get
        every valid spelling instead of just this default one."""
        assert_typing(chromatic, cls.ChromaticClass)
        diatonic = cls.DiatonicClass([0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                             chromatic.in_base_octave().value] + 7 * chromatic.octave())
        return cls(chromatic, diatonic)

    @classmethod
    def all_from_chromatic(cls, chromatic: ChromaticType) -> List["Pair"]:
        """Return every `Pair` (i.e. every valid diatonic spelling, such as C#/Db, or B#/C/Dbb) that
        shares the given chromatic value, within one octave of enharmonic spellings."""
        assert_typing(chromatic, cls.ChromaticClass)
        diatonic_array = [
            [0, -1, 1], #C, B#, Dbb
            [0, 1],  # C#, Db
            [1, 0, 2], # D, C##, Ebb 
            [2, 1], #  Eb, D#
            [2, 3, 1], # E, Fb, D##
            [3, 2, 4], # F, E#, Gbb
            [3, 4], # F#, Gb
            [4, 3, 5], #G, F##, Abb
            [5, 4], # Ab, G#
            [5, 6, 4], # A, Bbb, G##s 
            [6, 5], # Bb, A#
            [6, 7, 5], # B, Cb, A## 
            ]
        diatonics = [cls.DiatonicClass(diatonic + 7 * chromatic.octave()) 
                     for diatonic in diatonic_array[chromatic.in_base_octave().value]]
        return [cls(chromatic, diatonic) for diatonic in diatonics]

    @classmethod
    def from_diatonic(cls, diatonic: DiatonicType, scale: str="Major") -> "Pair":
        """Return the `Pair` combining `diatonic` with the chromatic value it has in `scale` (only
        "Major" is currently supported, i.e. no sharps/flats)."""
        assert_typing(diatonic, cls.DiatonicClass)
        assert scale == "Major"
        chromatic = cls.ChromaticClass.make([0, 2, 4, 5, 7, 9, 11][
                                             diatonic.in_base_octave().value] + 12 * diatonic.octave())
        return cls.make(chromatic, diatonic)

    def __eq__(self, other: "Pair") -> bool:
        """Two pairs are equal iff both their diatonic and chromatic components are equal (so G# != Ab)."""
        diatonicEq = self._diatonic == other._diatonic
        chromaticEq = self.get_chromatic() == other.get_chromatic()
        return diatonicEq and chromaticEq

    def _get_alteration_value(self) -> int:
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
        diatonic = self.get_diatonic()
        chromatic_from_diatonic = self.__class__.from_diatonic(diatonic).get_chromatic()
        return self.get_chromatic().value - chromatic_from_diatonic.value

    def get_alteration(self, throw: bool = True) -> AlterationType:
        """The alteration, added to `self.getDiatonic()` to obtain `self`
        
        If `throw` is False, return a Alteration which should not exists instead of raising"""
        from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
        value = self._get_alteration_value()
        try:
            return self.get_alteration_constructor()(value)
        except TooBigAlterationException as tba:
            if not throw:
                return WrongAlteration.make(value)
            tba["The note which is too big"] = self
            raise

    def __repr__(self) -> str:
        """Evaluable repr, e.g. `Note.make(0, 0)`, reusing the raw chromatic/diatonic int values."""
        return f"{self.__class__.__name__}.make({self.get_chromatic().value}, {self._diatonic.value})"

    def __le__(self, other: "Pair") -> bool:
        """Ordered by (chromatic, diatonic), chromatic taking precedence."""
        assert_typing(other, self.__class__)
        return (self.get_chromatic(), self._diatonic) <= (other.get_chromatic(), other._diatonic)

    def __lt__(self, other: "Pair") -> bool:
        """Ordered by (chromatic, diatonic), chromatic taking precedence."""
        assert_typing(other, self.__class__)
        return (self.get_chromatic(), self._diatonic) < (other.get_chromatic(), other._diatonic)

    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        """The `(chromatic_value, diatonic_value)` tuple, as text, used by `MakeableWithSingleArgument`."""
        return f"""{self.get_chromatic().value, self._diatonic.value}"""

    @classmethod
    def _make_single_argument(cls, arg: Union[Tuple[int, int], int]) -> "Pair":
        """If there are two arguments, it's chromatic, diatonic. If there is a single arg, it's chromatic, diatonic is one (useful for most scale). If it's already a Pair, return it."""
        if isinstance(arg, tuple):
            assert 2<=len(arg) <= 3
            return cls.make(*arg)
        assert_typing(arg, int)
        return cls.make(arg, 1)
    
    #pragma mark - ChromaticGetter

    def get_chromatic(self) -> ChromaticType:
        """Return the chromatic component of this pair."""
        return self._chromatic

    #pragma mark - DiatonicGetter

    def get_diatonic(self) -> DiatonicType:
        """Return the diatonic component of this pair."""
        return self._diatonic

    #pragma mark - Abstract

    def octave(self) -> int:
        """The octave, derived from the diatonic component (see `Singleton.octave`)."""
        return self._diatonic.octave()

    @classmethod
    def one_octave(cls)-> Self:
        """The pair representing exactly one octave (both components at their own `one_octave()`)."""
        return cls.make_instance_of_selfs_class(_chromatic=cls.ChromaticClass.one_octave(), _diatonic=cls.DiatonicClass.one_octave())

    # must be implemented by subclasses
    @abstractmethod
    def get_alteration_constructor(self) -> Callable[[int], AlterationType]:
        """Return the callable used to build this pair's `AlterationType` from an int alteration value."""
        ...

    # Pragma mark - DataClassWithDefaultArgument
    def __post_init__(self) -> None:
        """Validate that the chromatic/diatonic components are instances of this class's declared
        `ChromaticClass`/`DiatonicClass`."""
        assert_typing(self.get_chromatic(), self.ChromaticClass)
        assert_typing(self._diatonic, self.DiatonicClass)
        super().__post_init__()

    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict) -> Tuple[List, Dict]:
        """Coerce the `_chromatic`/`_diatonic` constructor arguments via each component class's
        `make_single_argument`, so e.g. a bare int can be passed instead of a full `Chromatic` instance."""
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_chromatic", cls.ChromaticClass.make_single_argument)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_diatonic", cls.DiatonicClass.make_single_argument)
        return args, kwargs