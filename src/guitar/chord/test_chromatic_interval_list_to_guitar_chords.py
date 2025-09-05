import unittest

from .chromatic_interval_list_to_guitar_chords import * 
from .test_constants import *
from solfege.pattern.chord.chord_patterns import major_triad


class TestChromaticIntervalListToGuitarChord(unittest.TestCase):
    def test_iter(self):
        itv_to_chord = ChromaticIntervalListToGuitarChords.make()
        itv_to_chord.maybe_register(F)
        all_interval_and_its_inversions = list(itv_to_chord)
        self.assertEqual(len(all_interval_and_its_inversions), 1) 
        interval_list, chromatic_interval_list_and_its_guitar_chords = all_interval_and_its_inversions[0]
        self.assertIsInstance(interval_list, ChromaticIntervalList)
        self.assertIsInstance(chromatic_interval_list_and_its_guitar_chords, ChromaticIntervalListAndItsGuitarChords)
        guitar_chords = chromatic_interval_list_and_its_guitar_chords.guitar_chords
        self.assertEqual(guitar_chords, [F])
        interval_and_its_inversions = chromatic_interval_list_and_its_guitar_chords.interval_and_its_inversions
        self.assertIsInstance(interval_and_its_inversions, ChromaticIntervalListAndItsInversions)
        inversions = interval_and_its_inversions.inversions
        self.assertEqual(len(inversions), 1)
        inversion = inversions[0]
        self.assertEqual(inversion.inversion, 0)
        self.assertEqual(inversion.base, major_triad)
        