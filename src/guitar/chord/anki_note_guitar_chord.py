from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from guitar.chord.guitar_chord import GuitarChord
from solfege.pattern.chord.inversion_pattern import InversionPattern


@dataclass
class AnkiNoteGuitarChord:
    inversion_to_guitar_chord: ClassVar[Dict[InversionPattern, "AnkiNoteGuitarChord"]] = dict()
    inversion: InversionPattern
    chords: List[GuitarChord] = field(default_factory=list)

    @classmethod
    def register(cls, inversion: InversionPattern, guitar_chord: GuitarChord):
        if inversion not in cls.inversion_to_guitar_chord:
            cls.inversion_to_guitar_chord[inversion] = AnkiNoteGuitarChord()
        cls.inversion_to_guitar_chord[inversion].chords.append(guitar_chord)

    
    