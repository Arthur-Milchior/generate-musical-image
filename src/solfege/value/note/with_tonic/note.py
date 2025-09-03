
from dataclasses import dataclass
from typing import Self, Union
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note, DiatonicNote, ChromaticNote
from solfege.value.note.with_tonic.abstract import AbstractNoteWithTonic
from solfege.value.note.with_tonic.chromatic import ChromaticNoteWithTonic
from solfege.value.note.with_tonic.diatonic import DiatonicNoteWithTonic


@dataclass(frozen=True, eq=False)
class NoteWithTonic(AbstractNoteWithTonic, Note):
    """A note of the scale, as an interval from middle C."""

    @classmethod
    def make(cls,
            chromatic: Union[ChromaticNote, int],
            diatonic: Union[DiatonicNote, int],
            tonic: Union[AbstractNoteWithTonic, bool]) -> Self:
        if isinstance(chromatic, int):
            chromatic = ChromaticNote(chromatic)    
        if isinstance(diatonic, int):
            diatonic = DiatonicNote(diatonic)    
        return cls(chromatic=chromatic, diatonic=diatonic, tonic=tonic)
    #
    # def get_interval_name(self, forFile=None):
    #     """The name of this note.
    #
    #     Args: `forFile` -- whether we should avoid non ascii symbol"""
    #     diatonic = self.get_diatonic()
    #     try:
    #         alteration = self.get_alteration()
    #     except TooBigAlteration as tba:
    #         tba.addInformation("Note", self)
    #         raise
    #     diatoànicName = diatonic.get_interval_name().upper()
    #     alterationName = alteration.get_interval_name(forFile=forFile)
    #     return "%s%s" % (diatonicName, alterationName)
    #
    # def correctAlteration(self):
    #     return self.get_alteration().printable()

    def _add(self, other: Interval) -> Self:
        sum: Note = super()._add(other)
        tonic = self.get_tonic()
        return self.__class__(chromatic = sum.chromatic, diatonic=sum.diatonic, tonic=tonic)


ChromaticNoteWithTonic.DiatonicClass = DiatonicNoteWithTonic
DiatonicNoteWithTonic.ChromaticClass = ChromaticNoteWithTonic
ChromaticNoteWithTonic.PairClass = NoteWithTonic