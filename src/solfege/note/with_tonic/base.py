from __future__ import annotations

import unittest
from typing import Dict, Optional, Union

from solfege.interval.abstract import AbstractInterval
from solfege.note.abstract import AbstractNote


class _NoteWithFundamental(AbstractNote):
    """
    Classes for note with base. They are a note, with an additional property representing the tonic.
    If `tonic` is `True`, then `self` is the tonic.
    """

    role: Dict[Optional[str]]
    _fundamental: Optional[_NoteWithFundamental]

    def __init__(self, fundamental: Union[bool, _NoteWithFundamental] = False,
                 **kwargs):
        """
        Same as the note type we inherit.
        Plus the tonic of the scale we are considering here."""
        self._fundamental = None
        super().__init__(**kwargs)
        if isinstance(fundamental, _NoteWithFundamental):
            self.set_tonic(fundamental)
        elif fundamental is True:
            self._fundamental = self
        else:
            assert (fundamental is False)
            self._fundamental = None

    def __add__(self, other: AbstractInterval) -> _NoteWithFundamental:
        sum_ = super().__add__(other)
        tonic = self.get_tonic()
        if tonic is not None:
            sum_.set_tonic(tonic)
        return sum_

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: _NoteWithFundamental):
        # Testing with get_number because the tonic of the tonic is itself, so no need to recurse
        if not super().__eq__(other):
            return False
        if self.get_tonic() is None:
            return other.get_tonic() is None
        if other.get_tonic() is None:
            return False
        return self.get_tonic().get_number() == other.get_tonic().get_number()

    def __sub__(self, other: Union[_NoteWithFundamental, AbstractInterval]):
        if isinstance(other, _NoteWithFundamental):
            assert (self.get_tonic() == other.get_tonic())
        return super().__sub__(other)

    def set_tonic(self, fundamental: _NoteWithFundamental):
        assert (self._fundamental is None)
        assert (fundamental.get_tonic() == fundamental)
        self._fundamental = fundamental
        if self.__class__ != fundamental.__class__:
            raise Exception("Adding a base of a type {base.__class__} distinct from the class {self.__class__}")

    def get_interval(self):
        """interval between the note and its base"""
        if "interval" not in self.dic:
            if self._fundamental is None or self.value is None:
                self.dic["interval"] = None
            else:
                self.dic["interval"] = self - self._fundamental
        return self.dic["interval"]

    def get_role(self):
        """The role of this note, assuming it's in a major scale"""
        if "role" not in self.dic:
            interval = self.get_interval()
            interval = interval.get_number() % self.number_of_interval_in_an_octave
            role = self.role[interval]
            self.dic["role"] = role
        return self.dic["role"]

    def get_tonic(self) -> _NoteWithFundamental:
        return self._fundamental

    def __repr__(self):
        return f"""{self.__class__.__name__}(value={self.get_number()}, repr={"self" if self._fundamental is self else repr(self._fundamental)})"""


