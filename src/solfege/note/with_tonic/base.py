from __future__ import annotations

import unittest
from typing import Dict, Optional, Union

from solfege.interval.abstract import AbstractInterval
from solfege.note.abstract import AbstractNote


class _NoteWithFundamental(AbstractNote):
    """
    Classes for notes with base. They are a note, with an additional property representing the tonic.
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


class TestNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = _NoteWithFundamental(value=1, fundamental=True)
        n1_1_ = _NoteWithFundamental(value=1, fundamental=True)
        self.assertEquals(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = _NoteWithFundamental(value=1, fundamental=True)
        n2_1 = _NoteWithFundamental(value=2, fundamental=n1_1)
        n2_2 = _NoteWithFundamental(value=2, fundamental=True)
        n3_1 = _NoteWithFundamental(value=3, fundamental=n1_1)
        self.assertNotEquals(n2_1, n2_2)
        self.assertNotEquals(n3_1, n2_1)

    def test_self_tonic(self):
        n = _NoteWithFundamental(value=1, fundamental=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = _NoteWithFundamental(value=1, fundamental=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=False)
        n2.set_tonic(n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = n1 + AbstractInterval(value=2)
        self.assertEquals(n2.get_tonic(), n1)
        self.assertEquals(n2.get_number(), 3)
        self.assertEquals(n2, _NoteWithFundamental(value=3, fundamental=n1))
        with self.assertRaises(Exception):
            _ = n1 + n1

    def test_sub_note(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        diff = n2 - n1
        self.assertEquals(diff, AbstractInterval(1))
        with self.assertRaises(Exception):
            _ = n1 - _NoteWithFundamental(value=1, fundamental=n2)

    def test_sub_interval(self):
        n1 = _NoteWithFundamental(value=1, fundamental=True)
        n2 = _NoteWithFundamental(value=2, fundamental=n1)
        self.assertEquals(n1 - AbstractInterval(1), _NoteWithFundamental(value=0, fundamental=n1))
        self.assertEquals(n2 - AbstractInterval(1), _NoteWithFundamental(value=1, fundamental=n1))
