import unittest

from guitar.chord.open.chromatic_note_list_and_its_guitar_chords import ChromaticNoteListAndItsGuitarChords
from guitar.position.test_set_of_guitar_positions import CM, CM_
from solfege.pattern.chord.chord_patterns import major_triad
from solfege.value.note.note import Note
from solfege.pattern.chord.test_chromatic_intervals_and_its_inversions import major_chromatic_interval_list_and_its_inversion

C4 = Note.make(0, 0)
class TestChromaticListAndItsGuitarChords(unittest.TestCase):
    def test_maximals(self):
        c_major = major_triad.from_note(C4)
        cnlaigc = ChromaticNoteListAndItsGuitarChords.make(
            interval_and_its_inversions= major_chromatic_interval_list_and_its_inversion,
            lowest_note=C4.get_chromatic())
        cnlaigc.append(CM_)
        cnlaigc.append(CM)
        maximals = cnlaigc.maximals()
        self.assertEqual(len(maximals), 1)
        maximal = maximals[0]
        self.assertEqual(CM, maximal)