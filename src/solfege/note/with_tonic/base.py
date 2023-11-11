from __future__ import annotations

import unittest
from typing import Dict, Optional, Union

from solfege.interval.base import _Interval
from solfege.note.base import _Note


class _NoteWithTonic(_Note):
    """
    Classes for notes with base. They are a note, with an additional property representing the tonic.
    If `tonic` is `True`, then `self` is the tonic.
    """

    role: Dict[Optional[str]]
    _tonic: Optional[_NoteWithTonic]

    def __init__(self, toCopy: Optional[_NoteWithTonic] = None, tonic: Union[bool, _NoteWithTonic] = False,
                 **kwargs):
        """
        Same as the note type we inherit.
        Plus the tonic of the scale we are considering here."""
        self._tonic = None
        super().__init__(toCopy=toCopy, **kwargs)
        if isinstance(toCopy, _NoteWithTonic):
            tonic = toCopy.get_tonic()
            assert (tonic is False)
            return
        if isinstance(tonic, _NoteWithTonic):
            self.set_tonic(tonic)
        elif tonic is True:
            self._tonic = self
        else:
            assert (tonic is False)
            self._tonic = None

    def __add__(self, other: _Interval) -> _NoteWithTonic:
        sum_ = super().__add__(other)
        tonic = self.get_tonic()
        if tonic is not None:
            sum_.set_tonic(tonic)
        return sum_

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        # Testing with get_number because the tonic of the tonic is itself, so no need to recurse
        return super().__eq__(other) and self.get_tonic().get_number() == other.get_tonic().get_number()

    def __sub__(self, other: Union[_NoteWithTonic, _Interval]):
        if isinstance(other, _NoteWithTonic):
            assert (self.get_tonic() == other.get_tonic())
        return super().__sub__(other)

    def set_tonic(self, tonic: _NoteWithTonic):
        assert (self._tonic is None)
        assert (tonic.get_tonic() == tonic)
        self._tonic = tonic
        if self.__class__ != tonic.__class__:
            raise Exception("Adding a base of a type {base.__class__} distinct from the class {self.__class__}")

    def get_interval(self):
        """interval between the note and its base"""
        if "interval" not in self.dic:
            if self._tonic is None or self.value is None:
                self.dic["interval"] = None
            else:
                self.dic["interval"] = self - self._tonic
        return self.dic["interval"]

    def get_role(self):
        """The role of this note, assuming it's in a major scale"""
        if "role" not in self.dic:
            interval = self.get_interval()
            interval = interval.get_number() % self.modulo
            role = self.role[interval]
            self.dic["role"] = role
        return self.dic["role"]

    def get_tonic(self) -> _NoteWithTonic:
        return self._tonic


class TestNoteWithTonic(unittest.TestCase):
    def test_eq(self):
        n1_1 = _NoteWithTonic(value=1, tonic=True)
        n1_1_ = _NoteWithTonic(value=1, tonic=True)
        self.assertEquals(n1_1, n1_1_)

    def test_ne(self):
        n1_1 = _NoteWithTonic(value=1, tonic=True)
        n2_1 = _NoteWithTonic(value=2, tonic=n1_1)
        n2_2 = _NoteWithTonic(value=2, tonic=True)
        n3_1 = _NoteWithTonic(value=3, tonic=n1_1)
        self.assertNotEquals(n2_1, n2_2)
        self.assertNotEquals(n3_1, n2_1)

    def test_self_tonic(self):
        n = _NoteWithTonic(value=1, tonic=True)
        self.assertIs(n, n.get_tonic())

    def test_self_no_tonic(self):
        n = _NoteWithTonic(value=1, tonic=False)
        self.assertIsNone(n.get_tonic())

    def test_self_set_tonic(self):
        n1 = _NoteWithTonic(value=1, tonic=True)
        n2 = _NoteWithTonic(value=2, tonic=False)
        n2.set_tonic(n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_self_init_tonic(self):
        n1 = _NoteWithTonic(value=1, tonic=True)
        n2 = _NoteWithTonic(value=2, tonic=n1)
        self.assertEquals(n2.get_tonic(), n1)

    def test_single_set(self):
        n1 = _NoteWithTonic(value=1, tonic=True)
        n2 = _NoteWithTonic(value=2, tonic=n1)
        with self.assertRaises(Exception):
            n2.set_tonic(n1)
        with self.assertRaises(Exception):
            n1.set_tonic(n1)

    def test_add(self):
        n1 = _NoteWithTonic(value=1, tonic=True)
        n2 = n1 + _Interval(value=2)
        self.assertEquals(n2.get_tonic(), n1)
        self.assertEquals(n2.get_number(), 3)

    def test_sub_note(self):
        n1 = _NoteWithTonic(value=1, tonic=True)
        n2 = _NoteWithTonic(value=2, tonic=n1)
        diff = n2 - n1
        self.assertEquals(diff, _Interval(1))
        with self.assertRaises(Exception):
            _ = n1 - _NoteWithTonic(value=1, tonic=n2)

    def test_sub_interval(self):
        n = _NoteWithTonic(value=1, tonic=True)
        self.assertEquals(n - _Interval(1), _NoteWithTonic(value=0, tonic=n))
