from __future__ import annotations

import math
from typing import Self, TypeVar


class AbstractInterval:
    """This class is the basis for each kind of interval. It should never be used directly.
    It allows to represent a number, access it.
    It also allows to add it to another such element, negate it, while generating an object of its subclass.
    Such elements can be compared, and basically hashed (the hash being the number itself)

    The number can't be set, because the object is supposed to be immutable.

    Inheriting class which are instantiated should contain the following variable:
    * modulo: number of note by octave (7 for diatonic, 12 for chromatic)
    * ClassToTransposeTo: the class of object to generate. If it's None, the class of self is used.
    * RelatedDiatonicClass: class to which a chromatic object must be converted when a diatonic object is required.
    * RelatedSolfegeClass: the class to which a diatonic and chromatic object must be converted.
"""
    ClassToTransposeTo = None
    number_of_interval_in_an_octave: int
    IntervalClass: type[AbstractInterval]
    value: int

    def __init__(self, value: int, **kwargs):
        """If the interval is passed as argument, it is copied. Otherwise, the value is used."""
        super().__init__(**kwargs)
        assert isinstance(value, int)
        self.value = value

    def is_note(self) -> bool:
        """True if it's a note. False if it's an interval"""
        return False

    def has_number(self):
        return isinstance(self.value, int)

    def get_number(self) -> int:
        if not isinstance(self.value, int):
            raise Exception("A number which is not int but %s" % self.value)
        return self.value

    @classmethod
    def get_one_octave(cls) -> Self:
        return cls.IntervalClass(value=cls.number_of_interval_in_an_octave)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise Exception(f"Comparison of two distinct classes: {self.__class__} and {other.__class__}")
        return self.get_number() == other.get_number()

    def __add__(self, other: AbstractInterval) -> Self:
        """Sum of both intervals. Class of `self`"""
        from solfege.note.abstract import AbstractNote
        if isinstance(other, AbstractNote):
            cls = other.__class__
        else:
            cls = self.__class__
        if not isinstance(other, int):
            other_number = other.get_number()
        else:
            other_number = other
        sum_ = self.get_number() + other_number
        ret = cls(value=sum_)
        return ret

    def __rmul__(self, other) -> Self:
        return self.__mul__(other)

    def __mul__(self, other) -> Self:
        assert (isinstance(other, int))
        from solfege.note.abstract import AbstractNote
        assert (not isinstance(self, AbstractNote))
        cls = self.ClassToTransposeTo or self.__class__
        return cls(value=self.get_number() * other)

    def __neg__(self) -> Self:
        """Inverse interval"""
        cls = self.ClassToTransposeTo or self.__class__
        return cls(value=-self.get_number())

    def __sub__(self, other: AbstractInterval) -> Self:
        """This interval minus the other one. Class of `self`"""
        neg = -other
        if neg.is_note():
            raise Exception("Neg is %s, which is a note" % neg)
        return self + neg

    def __hash__(self):
        return self.get_number()

    def __le__(self, other):
        if isinstance(other, AbstractInterval):
            other = other.get_number()
        return self.get_number() <= other

    def __lt__(self, other):
        if isinstance(other, AbstractInterval):
            other = other.get_number()
        return self.get_number() < other

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.get_number()})"

    def get_octave(self):
        """The octave number. 0 for unison/central C up to seventh/C one octave above."""
        return math.floor(self.get_number() / self.__class__.number_of_interval_in_an_octave)

    def add_octave(self, nb: int) -> Self:
        """Same note with nb more octave"""
        return self + self.get_one_octave() * nb

    def get_in_base_octave(self) -> Self:
        """Same note in the base octave"""
        return self.add_octave(-self.get_octave())

    def equals_modulo_octave(self, other) -> bool:
        """Whether self and other are same note, potentially at distinct octaves"""
        return self.get_in_base_octave() == other.get_in_base_octave()

    def difference_in_base_octave(self, other):
        """self-other, in octave"""
        cls = self.ClassToTransposeTo or self.__class__
        return cls((self.get_number() - other.get_number()) % self.__class__.number_of_interval_in_an_octave)


IntervalType = TypeVar('IntervalType', bound=AbstractInterval)


