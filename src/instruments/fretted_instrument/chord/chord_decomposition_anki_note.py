from dataclasses import dataclass, field
from tkinter.font import names
from typing import List

from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordColors, ChordOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors
from solfege.pattern.inversion.chromatic_identical_inversion_patterns import MinimalChordDecompositionInput
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from utils.csv import CsvGenerator
from utils.easyness import ClassWithEasyness
from utils.frozenlist import StrFrozenList
from utils.util import assert_iterable_typing, assert_typing, img_tag

@dataclass(frozen=True)
class ChordDecompositionAnkiNote(ClassWithEasyness, CsvGenerator):
    instrument: FrettedInstrument
    identical_inversions: MinimalChordDecompositionInput
    chord: ChordOnFrettedInstrument

    def __post_init__(self):
        assert_typing(self.instrument, FrettedInstrument)
        assert_typing(self.identical_inversions, MinimalChordDecompositionInput)
        assert_typing(self.chord, ChordOnFrettedInstrument)

    def is_open(self):
        return self.chord.is_open()

    def transposed(self):
        """The chord as it should be presented as svg, and the transposition compared to `chord`."""
        if self.is_open():
            return self.chord, ChromaticInterval(0)
        return self.chord.transpose_to_fret_one()

    #pragma mark - CsvGenerator

    def csv_content(self, folder_path: str) -> List[str]:
        transposed, transposition = self.transposed()
        notations = self.identical_inversions.notations()
        tonic_minus_lowest_note = self.identical_inversions.get_tonic_minus_lowest_note()
        lowest_note = self.chord.get_most_grave_note().get_chromatic()
        tonic = lowest_note - tonic_minus_lowest_note
        colors = ChordColors(tonic)
        fields = []
        absolute = transposed.is_open()
        fields.append(notations[0])
        fields.append(", ".join(notations[1:]))
        fields.append(img_tag(transposed.save_svg(folder_path, self.instrument, colors=None, absolute=absolute)))
        fields.append(img_tag(transposed.save_svg(folder_path, self.instrument, colors=colors, absolute=absolute)))
        for interval_values in [[0], [1, 2], [3, 4], [5], [6, 7, 8], [9, 10, 11]]:
            intervals = [ChromaticInterval(iv) for iv in interval_values]
            notes = [tonic + interval for interval in intervals]
            notes_in_base_octave = [note.in_base_octave() for note in notes]
            restricted_chord = transposed.restricte_to_note_up_to_octave(notes_in_base_octave)
            if restricted_chord is None:
                fields.append("")
            else:
                fields.append(img_tag(restricted_chord.save_svg(folder_path, self.instrument, colors=colors, absolute=absolute)))
        return fields

    #pragma mark - ClassWithEasyness

    def easy_key(self):
        return (self.identical_inversions.easy_key(), self.chord.easy_key())