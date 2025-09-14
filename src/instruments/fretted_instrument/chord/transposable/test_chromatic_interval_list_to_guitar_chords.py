import unittest

from solfege.pattern.inversion.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions

from .inversion_pattern_to_chords_on_fretted_instrument import * 
from ..test_constants import *
from solfege.pattern.chord.chord_patterns import major_triad


class TestChromaticIntervalListToFrettedInstrumentChord(unittest.TestCase):
    def test_iter(self):
        itv_to_chord = ChromaticIntervalListToFrettedInstrumentChords.make(Guitar)
        chromatic_intervals = F4M.intervals_frow_lowest_note_in_base_octave()
        itv_to_chord.register(chromatic_intervals, F4M)
        all_interval_and_its_inversions = list(itv_to_chord)
        self.assertEqual(len(all_interval_and_its_inversions), 1) 
        interval_list, chromatic_interval_list_and_its_fretted_instrument_chords = all_interval_and_its_inversions[0]
        self.assertIsInstance(interval_list, ChromaticIntervalListPattern)
        self.assertIsInstance(chromatic_interval_list_and_its_fretted_instrument_chords, ChromaticIntervalListAndItsFrettedInstrumentChords)
        fretted_instrument_chords = chromatic_interval_list_and_its_fretted_instrument_chords.fretted_instrument_chords
        self.assertEqual(fretted_instrument_chords, [F4M])
        interval_and_its_inversions = chromatic_interval_list_and_its_fretted_instrument_chords.interval_and_its_inversions
        self.assertIsInstance(interval_and_its_inversions, ChromaticIntervalListAndItsInversions)
        inversions = interval_and_its_inversions.inversions
        self.assertEqual(len(inversions), 1)
        inversion = inversions[0]
        self.assertEqual(inversion.inversion, 0)
        self.assertEqual(inversion.base, major_triad)
        