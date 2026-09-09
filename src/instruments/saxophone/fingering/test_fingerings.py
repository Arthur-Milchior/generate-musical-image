import unittest

from instruments.saxophone.fingering import saxophone_fingerings

from instruments.saxophone.fingering import cn
from instruments.saxophone.fingering.cn import cn_silent
from instruments.saxophone.fingering import k
from instruments.saxophone.fingering.k import k_silent
from instruments.saxophone.fingering.main_column import silent
from instruments.saxophone.fingering.saxophone_fingering import *
from instruments.saxophone.fingering import rascher
from instruments.saxophone.fingering.overtone import overtone


class TestFingerings(unittest.TestCase):
    """Sanity checks that the catalog built in `saxophone_fingerings.py` matches what's expected for a sample
    note (`e6`): the right alternates, in the right order, with the right buttons."""

    def test_e6(self):
        """`saxophone_fingerings.e6` contains exactly the expected alternate fingerings, in order, and its
        first (`cn.e6_k`) fingering presses the expected buttons."""
        ordered_fingerings = list(saxophone_fingerings.e6)
        expected_fingerings = [cn.e6_k, overtone.e6_A, cn.e6_t, main_column.e6_d]
        self.assertEqual(ordered_fingerings, expected_fingerings)
        expect_e6_k = SaxophoneFingering.make("e6", {jay_H1, jay_H2, octave, jay_k4}, test=True)
        self.assertEqual(expect_e6_k, cn.e6_k)
        print(cn.e6_k.svg())