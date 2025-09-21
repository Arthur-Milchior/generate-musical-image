from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, ClassVar, Dict, Generic, List, Self, Tuple, Type, Union

from solfege.value.abstract import Abstract
from solfege.value.chromatic import Chromatic, ChromaticGetter, ChromaticType
from solfege.value.diatonic import Diatonic, DiatonicGetter, DiatonicType
from solfege.value.interval.alteration.alteration import Alteration, AlterationType
from utils.frozenlist import MakeableWithSingleArgument
from utils.util import assert_typing


@dataclass(frozen=True, unsafe_hash=True)
class Pair(Abstract, MakeableWithSingleArgument, ChromaticGetter, DiatonicGetter, Generic[ChromaticType, DiatonicType, AlterationType]):
    """How to generate a new Pair, from chromatic and diatonic"""
    DiatonicClass: ClassVar[Type[Diatonic]] = Diatonic
    ChromaticClass: ClassVar[Type[Chromatic]] = Chromatic
    IntervalClass: ClassVar[Type["Pair"]]

    _chromatic: ChromaticType
    _diatonic: DiatonicType

    @classmethod
    def make_instance_of_selfs_class(cls: Type["Pair"], _chromatic: ChromaticType, _diatonic: DiatonicType):
        return cls.make(_chromatic, _diatonic)

    @classmethod
    def from_chromatic(cls, chromatic: ChromaticType):
        assert_typing(chromatic, cls.ChromaticClass)
        diatonic = cls.DiatonicClass([0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6][
                                             chromatic.in_base_octave().value] + 7 * chromatic.octave())
        return cls(chromatic, diatonic)

    @classmethod
    def all_from_chromatic(cls, chromatic: ChromaticType):
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
    def from_diatonic(cls, diatonic: DiatonicType, scale: str="Major"):
        assert_typing(diatonic, cls.DiatonicClass)
        assert scale == "Major"
        chromatic = cls.ChromaticClass([0, 2, 4, 5, 7, 9, 11][
                                             diatonic.in_base_octave().value] + 12 * diatonic.octave())
        return cls(chromatic, diatonic)

    def __eq__(self, other: "Pair"):
        diatonicEq = self._diatonic == other._diatonic
        chromaticEq = self._chromatic == other._chromatic
        return diatonicEq and chromaticEq

    def _get_alteration_value(self) -> int:
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
        diatonic = self.get_diatonic()
        chromatic_from_diatonic = self.__class__.from_diatonic(diatonic)._chromatic
        return self._chromatic.value - chromatic_from_diatonic.value

    def get_alteration(self) -> AlterationType:
        """The alteration, added to `self.getDiatonic()` to obtain `self`"""
        from solfege.value.interval.too_big_alterations_exception import TooBigAlterationException
        try:
            return self.get_alteration_constructor()(self._get_alteration_value())
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise

    def __repr__(self):
        return f"{self.__class__.__name__}.make({self._chromatic.value}, {self._diatonic.value})"

    def __le__(self, other: "Pair"):
        assert_typing(other, self.__class__)
        return (self._chromatic, self._diatonic) <= (other._chromatic, other._diatonic)

    def __lt__(self, other: "Pair"):
        assert_typing(other, self.__class__)
        return (self._chromatic, self._diatonic) < (other._chromatic, other._diatonic)

    #pragma mark - MakeableWithSingleArgument

    def repr_single_argument(self) -> str:
        return f"""{self._chromatic.value, self._diatonic.value}"""

    @classmethod
    def _make_single_argument(cls, arg: Union[Tuple[int, int], int]):
        """If there are two arguments, it's chromatic, diatonic. If there is a single arg, it's chromatic, diatonic is one (useful for most scale). If it's already a Pair, return it."""
        if isinstance(arg, tuple):
            assert 2<=len(arg) <= 3
            return cls.make(*arg)
        assert_typing(arg, int)
        return cls.make(arg, 1)
    
    #pragma mark - ChromaticGetter

    def get_chromatic(self):
        return self._chromatic
    
    #pragma mark - DiatonicGetter

    def get_diatonic(self) -> DiatonicType:
        return self._diatonic
    
    #pragma mark - Abstract
    
    def octave(self):
        return self._diatonic.octave()

    @classmethod
    def one_octave(cls)-> Self:
        return cls.make_instance_of_selfs_class(_chromatic=cls.ChromaticClass.one_octave(), _diatonic=cls.DiatonicClass.one_octave())
    
    # must be implemented by subclasses
    @abstractmethod
    def get_alteration_constructor(self) -> Callable[[int], AlterationType]:...

    # Pragma mark - DataClassWithDefaultArgument
    def __post_init__(self):
        assert_typing(self._chromatic, self.ChromaticClass)
        assert_typing(self._diatonic, self.DiatonicClass)
        super().__post_init__()
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_chromatic", cls.ChromaticClass.make_single_argument)
        args, kwargs = cls.arg_to_kwargs(args, kwargs, "_diatonic", cls.DiatonicClass.make_single_argument)
        return args, kwargs