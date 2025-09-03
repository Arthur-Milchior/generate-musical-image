from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Type, Union

from solfege.value.interval.abstract_interval import AbstractInterval
from solfege.value.note.abstract_note import AbstractNote
from solfege.value.chromatic import Chromatic
from solfege.value.diatonic import Diatonic
from utils.util import assert_optional_typing, assert_typing


@dataclass(frozen=True)
class AbstractNoteWithTonic(AbstractNote):
    """
    Classes for note with tonic. They are a note, with an additional property representing the tonic.
    If `tonic` is `None`, then `self` is the tonic.
    """

    role: ClassVar[Dict[Optional[str]]]
    tonic: Union[AbstractNoteWithTonic, bool]
        
    def make_instance_of_selfs_class(self, *args, **kwargs):
        return self.__class__(*args, **kwargs, tonic=self.tonic)

    def __post_init__(self):
        super().__post_init__()
        assert isinstance(self.tonic, bool) or isinstance(self.tonic, AbstractNoteWithTonic)
        tonic = self.get_tonic()
        if tonic:
            assert self.get_tonic() == self.get_tonic().get_tonic()
        
    def get_tonic(self):
        if self.tonic is True:
            return self
        if self.tonic is False:
            return None
        return self.tonic

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: AbstractNoteWithTonic):
        # Testing with get_number because the tonic of the tonic is itself, so no need to recurse
        if not super().__eq__(other):
            return False
        return self.get_tonic()._equal_no_recursion(other.get_tonic())
    
    def _equal_no_recursion(self, other:AbstractNoteWithTonic):
        return super().__eq__(other)

    def __sub__(self, other: Union[AbstractNoteWithTonic, AbstractInterval]):
        if isinstance(other, AbstractNoteWithTonic):
            assert self.get_tonic() == other.get_tonic(), f"{self=}, {other=}"
        return super().__sub__(other)
    
    def is_tonic(self):
        return self is self.get_tonic()

    # def set_tonic(self, tonic: AbstractNoteWithTonic):
    #     assert self._tonic is None
    #     assert tonic.is_tonic(), f"{tonic=}"
    #     self._tonic = tonic
    #     if self.__class__ != tonic.__class__:
    #         raise Exception("Adding a tonic of a type {tonic.__class__} distinct from the class {self.__class__}")

    def get_interval(self):
        """interval between the note and its tonic"""
        if self.get_tonic() is None:
            return None
        else:
            return self - self.get_tonic()

    def get_role(self):
        """The role of this note, assuming it's in a major scale"""
        interval = self.get_interval()
        interval = interval.value % self.number_of_interval_in_an_octave
        return self.role[interval]

    def __repr__(self):
        return f"""{self.__class__.__name__}(value={self.value}, repr={"self" if self._tonic is self else repr(self._tonic)})"""


