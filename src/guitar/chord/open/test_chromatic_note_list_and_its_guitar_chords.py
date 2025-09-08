import unittest

from guitar.chord.open.chromatic_note_list_and_its_guitar_chords import ChromaticNoteListAndItsGuitarChords
from guitar.chord.test_guitar_chord import CM, CM_
from solfege.pattern.chord.chord_patterns import major_triad
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.note import Note
from solfege.pattern.chord.test_chromatic_intervals_and_its_inversions import major_chromatic_interval_list_and_its_inversion

class TestChromaticListAndItsGuitarChords(unittest.TestCase):
    def test_maximals(self):
        cnlaigc = ChromaticNoteListAndItsGuitarChords.make(
            interval_and_its_inversions= major_chromatic_interval_list_and_its_inversion,
            lowest_note=ChromaticNote(0))
        cnlaigc.append(CM_)
        cnlaigc.append(CM)
        maximals = cnlaigc.maximals()
        self.assertEqual(len(maximals), 1)
        maximal = maximals[0]
        self.assertEqual(CM, maximal)