import unittest

from solfege.pattern_instantiation.inversion.chromatic_inversion import ChromaticInversion
from solfege.pattern.chord.chord_patterns import major_triad
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList

class TestChord(unittest.TestCase):
    def test_generation(self):
        inversion = ChromaticInversion(major_triad.inversion(1), ChromaticNote(0))
        actual = inversion.get_notes()
        expected = ChromaticNoteFrozenList([0, 3, 8])
        self.assertEqual(expected, actual)
