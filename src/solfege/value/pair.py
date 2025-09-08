
from dataclasses import dataclass
from typing import Callable, ClassVar, Self, Tuple, Type, Union

from solfege.value.abstract import Abstract
from solfege.value.chromatic import Chromatic, ChromaticGetter
from solfege.value.diatonic import Diatonic, DiatonicGetter
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True, eq=False)
class Pair(Abstract, ChromaticGetter, DiatonicGetter):
    """How to generate a new Pair, from chromatic and diatonic"""
    make_instance_of_selfs_class: ClassVar[Callable[[int, int], "Pair"]]
    DiatonicClass: ClassVar[Type[Diatonic]] = Diatonic
    ChromaticClass: ClassVar[Type[Chromatic]] = Chromatic
    AlterationClass: ClassVar[Type[Chromatic]]
    IntervalClass: ClassVar[Type["Pair"]]

    chromatic: Chromatic
    diatonic: Diatonic

    def __post_init__(self):
        assert_typing(self.chromatic, self.ChromaticClass)
        assert_typing(self.diatonic, self.DiatonicClass)

    @classmethod
    def make_instance_of_selfs_class(cls: Type["Pair"], chromatic: Chromatic, diatonic: Diatonic):
        return cls(chromatic, diatonic)

    @classmethod
    def make(cls,
             chromatic: Union[Chromatic, int],
             diatonic: Union[Diatonic, int]) -> Self:
        if isinstance(chromatic, int):
            chromatic = cls.ChromaticClass(chromatic)
        if isinstance(diatonic, int):
            diatonic = cls.DiatonicClass(diatonic)
        return cls(chromatic, diatonic)
    
    @classmethod
    def make_single_argument(cls, arg: Union[Tuple[int, int], int, "Pair"]):
        """If there are two arguments, it's chromatic, diatonic. If there is a single arg, it's chromatic, diatonic is one (useful for most scale). If it's already a Pair, return it."""
        if isinstance(arg, tuple):
            assert len(arg) == 2
            chromatic, diatonic = arg
            return cls.make(chromatic, diatonic)
        if isinstance(arg, int):
            return cls.make(arg, 1)
        assert_typing(arg, cls)
        return arg

    def __eq__(self, other: "Pair"):
        diatonicEq = self.diatonic == other.diatonic
        chromaticEq = self.chromatic == other.chromatic
        return diatonicEq and chromaticEq

    def get_chromatic(self):
        return self.chromatic

    def get_diatonic(self) -> Diatonic:
        return self.diatonic

    def get_alteration(self) -> "Chromatic":
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
        diatonic = self.get_diatonic()
        chromatic_from_diatonic = diatonic.get_chromatic()
        try:
            return self.AlterationClass(self.chromatic.value - chromatic_from_diatonic.value)
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def __repr__(self):
        return f"{self.__class__.__name__}.make({self.chromatic.value}, {self.diatonic.value})"

    def _add(self, other: "Pair") -> Self:
        if not isinstance(other, Pair):
            return other._add(self)
        from solfege.value.interval.interval import Interval
        from solfege.value.note.note import Note
        assert self.IntervalClass == other.IntervalClass, f"{self.IntervalClass} != {other.IntervalClass}"
        diatonic = self.diatonic + other.diatonic
        chromatic = self.chromatic + other.chromatic
        if isinstance(other, Note):
            assert_typing(self, Interval)
            return other.make_instance_of_selfs_class(chromatic, diatonic)
        assert_typing(other, Interval)
        return self.make_instance_of_selfs_class(chromatic=chromatic, diatonic=diatonic)

    def __le__(self, other: "Pair"):
        assert_typing(other, self.__class__)
        return (self.chromatic, self.diatonic) <= (other.chromatic, other.diatonic)

    def __lt__(self, other: "Pair"):
        assert_typing(other, self.__class__)
        return (self.chromatic, self.diatonic) < (other.chromatic, other.diatonic)

    def octave(self):
        return self.diatonic.octave()