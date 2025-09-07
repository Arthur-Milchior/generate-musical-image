
from dataclasses import dataclass
from typing import Optional
from guitar.chord.chromatic_list_and_its_guitar_chords import ChromaticListAndItsGuitarChords
from guitar.chord.guitar_chord import GuitarChord
from lily import lily
from solfege.pattern.chord.inversion_pattern import InversionPattern
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.abstract_note import AlterationOutput, FixedLengthOutput, NoteOutput
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.set.note_list import NoteList
from utils.util import img_tag

@dataclass(frozen=True, unsafe_hash=True)
class ChromaticNoteListAndItsGuitarChords(ChromaticListAndItsGuitarChords[ChromaticNote]):
    """Up to octave"""
    lowest_note: ChromaticNote

    def chord_names(self):
        return [self.chord_name(inversion) for inversion in self.interval_and_its_inversions.inversions]

    def chord_name(self, inversion: InversionPattern):
        tonic: ChromaticNote = self.lowest_note - inversion.position_of_lowest_interval_in_base_octave.chromatic
        note_name = tonic.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        lowest_note_name = self.lowest_note.get_name_up_to_octave(alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO)
        chord_pattern_notation = inversion.base.notation
        if chord_pattern_notation is None:
            chord_pattern_notation = f" inversion.base.first_of_the_names()"
        chord_notation = f"{note_name}{chord_pattern_notation}"
        if inversion.inversion == 0:
            assert tonic == self.lowest_note
            return chord_notation
        else:
            return f"""{chord_notation}/{lowest_note_name}"""
    
    def notes(self, inversion: InversionPattern):
        notes_in_base_octave: NoteList = inversion.interval_list.from_note(self.lowest_note)
        return notes_in_base_octave.change_octave_to_be_enharmonic()
        
    def append(self, guitar_chord: GuitarChord):
        super().append(guitar_chord)
        assert guitar_chord.get_most_grave_note().get_chromatic().in_base_octave() == self.lowest_note.in_base_octave()
    
    def csv_content(self, lily_folder_path: Optional[str] = None):
        l = []
        inversions = self.interval_and_its_inversions.inversions
        easiest_inversion = inversions[0]
        other_inversions = inversions[1:]
        l.append(self.chord_name(easiest_inversion))
        l.append(", ".join(self.chord_name(inversion) for inversion in other_inversions))
        maximals = self.maximals()
        interval_list = easiest_inversion.interval_list
        for guitar_chord in maximals:
            l.append(img_tag(guitar_chord.file_name(stroke_colored=False)))
            l.append(img_tag(guitar_chord.file_name(stroke_colored=True)))
            note_list = guitar_chord.notes_from_interval_list(interval_list=interval_list)
            file_prefix = note_list.lily_file_name()
            if lily_folder_path:
                path_prefix = f"{lily_folder_path}/{file_prefix}"
                code = note_list.lily_file_with_only_chord()
                lily.compile_(code, path_prefix, wav=False)
            l.append(img_tag(f"{file_prefix}.svg"))
        for _ in range(7- len(maximals)):
            l.append("")
            l.append("")
            l.append("")
        return l