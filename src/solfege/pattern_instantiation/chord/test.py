import unittest

from solfege.list_order import ListOrder
from solfege.pattern_instantiation.inversion.chromatic_inversion_instantiation import ChromaticInversionInstantiation
from solfege.pattern.chord.chord_patterns import major_triad
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList
from solfege.value.note.set.chromatic_note_list import ChromaticNoteList

class TestChord(unittest.TestCase):
    def test_generation(self):
        inversion = ChromaticInversionInstantiation(major_triad.inversion(1), ChromaticNote(0))
        actual = inversion.get_notes()
        expected = ChromaticNoteList.make(notes=[0, 3, 8], list_order=ListOrder.INCREASING)
        self.assertEqual(expected, actual)
