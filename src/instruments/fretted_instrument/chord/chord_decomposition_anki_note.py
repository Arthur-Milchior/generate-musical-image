from dataclasses import dataclass
from tkinter.font import names
from typing import List

from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordColors, ChordOnFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions_with_fingers import ScaleColors
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.chromatic_note import ChromaticNote
from utils.csv import CsvGenerator
from utils.frozenlist import StrFrozenList
from utils.util import assert_iterable_typing, assert_typing, img_tag


@dataclass(frozen=True)
class ChordDecompositionAnkiNote(CsvGenerator):
    names: List[str]
    chord: ChordOnFrettedInstrument
    absolute: bool
    tonic: ChromaticNote

    def __post_init__(self):
        assert_iterable_typing(self.names, str)
        assert_typing(self.chord, ChordOnFrettedInstrument)
        assert_typing(self.absolute, bool)
        assert_typing(self.tonic, ChromaticNote)

    def transposed(self):
        """The chord as it should be presented as svg, and the transposition compared to `chord`."""
        if self.absolute:
            return self.chord, ChromaticInterval(0)
        return self.chord.transpose_to_fret_one()

    def csv_content(self, folder_path:str):
        chord, transposed = self.transposed()
        tonic = self.tonic + transposed
        colors = ChordColors(tonic)
        l= []
        l.append(self.names[0])
        l.append(", ".join(self.names[1:]))
        l.append(img_tag(chord.save_svg(folder_path, Guitar, colors=None, absolute=self.absolute)))
        l.append(img_tag(chord.save_svg(folder_path, Guitar, colors=colors, absolute=self.absolute)))
        for interval_values in [[0], [1, 2], [3, 4], [5], [6, 7, 8], [9, 10, 11]]:
            intervals = [ChromaticInterval(iv) for iv in interval_values]
            notes = [tonic + interval for interval in intervals]
            notes_in_base_octave = [note.in_base_octave() for note in notes]
            restricted_chord = chord.restricte_to_note_up_to_octave(notes_in_base_octave)
            if restricted_chord is None:
                l.append("")
            else:
                l.append(img_tag(restricted_chord.save_svg(folder_path, Guitar, colors=colors, absolute=self.absolute)))
        return l