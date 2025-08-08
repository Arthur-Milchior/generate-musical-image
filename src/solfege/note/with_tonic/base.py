from __future__ import annotations

from typing import Dict, Optional, Union

from solfege.interval.abstract import AbstractInterval
from solfege.note.abstract import AbstractNote


class AbstractNoteWithTonic(AbstractNote):
    """
    Classes for note with tonic. They are a note, with an additional property representing the tonic.
    If `tonic` is `True`, then `self` is the tonic.
    """

    role: Dict[Optional[str]]
    _tonic: Optional[AbstractNoteWithTonic]

    def __init__(self, tonic: Union[bool, AbstractNoteWithTonic] = False,
                 **kwargs):
        """
        Same as the note type we inherit.
        Plus the tonic of the scale we are considering here."""
        self._tonic = None
        super().__init__(**kwargs)
        if isinstance(tonic, AbstractNoteWithTonic):
            self.set_tonic(tonic)
        elif tonic is True:
            self._tonic = self
        else:
            assert (tonic is False)
            self._tonic = None

    def __add__(self, other: AbstractInterval) -> AbstractNoteWithTonic:
        sum_ = super().__add__(other)
        tonic = self.get_tonic()
        if tonic is not None:
            sum_.set_tonic(tonic)
        return sum_

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: AbstractNoteWithTonic):
        # Testing with get_number because the tonic of the tonic is itself, so no need to recurse
        if not super().__eq__(other):
            return False
        if self.get_tonic() is None:
            return other.get_tonic() is None
        if other.get_tonic() is None:
            return False
        return self.get_tonic().get_number() == other.get_tonic().get_number()

    def __sub__(self, other: Union[AbstractNoteWithTonic, AbstractInterval]):
        if isinstance(other, AbstractNoteWithTonic):
            assert self.get_tonic() == other.get_tonic(), f"{self=}, {other=}"
        return super().__sub__(other)
    
    def is_tonic(self):
        return self is self.get_tonic()

    def set_tonic(self, tonic: AbstractNoteWithTonic):
        assert (self._tonic is None)
        assert tonic.is_tonic(), f"{tonic=}"
        self._tonic = tonic
        if self.__class__ != tonic.__class__:
            raise Exception("Adding a tonic of a type {tonic.__class__} distinct from the class {self.__class__}")

    def get_interval(self):
        """interval between the note and its tonic"""
        if self._tonic is None or self.value is None:
            return None
        else:
            return self - self._tonic

    def get_role(self):
        """The role of this note, assuming it's in a major scale"""
        interval = self.get_interval()
        interval = interval.get_number() % self.number_of_interval_in_an_octave
        return self.role[interval]

    def get_tonic(self) -> AbstractNoteWithTonic:
        return self._tonic

    def __repr__(self):
        return f"""{self.__class__.__name__}(value={self.get_number()}, repr={"self" if self._tonic is self else repr(self._tonic)})"""


