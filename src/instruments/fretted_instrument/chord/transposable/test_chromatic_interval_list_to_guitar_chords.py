import unittest

from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern

from .inversion_pattern_to_chords_on_fretted_instrument import * 
from ..test_constants import *
from solfege.pattern.chord.chord_patterns import major_triad


class TestIdenticalInversionPatternToItsTransposableChords(unittest.TestCase):
    def test_iter(self):
        itv_to_chord = IdenticalInversionPatternToItsTransposableChords.make(instrument = Guitar)
        chromatic_intervals = F4M.intervals_frow_lowest_note_in_base_octave()
        identical_inversion_pattern = IdenticalInversionPatterns.make(IntervalListPattern.make_relative([(4, 2), (3, 2)]))
        identical_inversion_pattern.append(major_triad.inversion(0))

        itv_to_chord.register(identical_inversion_pattern, F4M)
        all_equivalent_patterns_and_its_inversions = list(itv_to_chord)
        self.assertEqual(len(all_equivalent_patterns_and_its_inversions), 1) 
        indentical_inversion_pattern_, chromatic_interval_list_and_its_fretted_instrument_chords = all_equivalent_patterns_and_its_inversions[0]
        self.assertIsInstance(indentical_inversion_pattern_, IdenticalInversionPatterns)
        self.assertIsInstance(chromatic_interval_list_and_its_fretted_instrument_chords, IdenticalInversionPatternAndItsTransposableChords)
        fretted_instrument_chords = chromatic_interval_list_and_its_fretted_instrument_chords.fretted_instrument_chords
        self.assertEqual(fretted_instrument_chords, [F4M])
        inversions = chromatic_interval_list_and_its_fretted_instrument_chords.key.get_identical_inversion_pattern().inversions
        self.assertEqual(len(inversions), 1)
        inversion = inversions[0]
        self.assertEqual(inversion.inversion, 0)
        self.assertEqual(inversion.base, major_triad)
        