import unittest

from saxophone.fingering import fingerings

from saxophone.fingering import cn
from saxophone.fingering.cn import cn_silent
from saxophone.fingering import k
from saxophone.fingering.k import k_silent
from saxophone.fingering.main_column import silent
from saxophone.fingering.fingering import *
from saxophone.fingering import rascher
from saxophone.fingering.overtone import overtone


class TestFingerings(unittest.TestCase):

    def test_e6(self):
        ordered_fingerings = list(fingerings.e6)
        expected_fingerings = [cn.e6_k, overtone.e6_A, cn.e6_t, main_column.e6_d]
        self.assertEqual(ordered_fingerings, expected_fingerings)
        expect_e6_k = Fingering("e6", {jay_H1, jay_H2, octave, jay_k4}, test=True)
        self.assertEqual(expect_e6_k, cn.e6_k)
        print(cn.e6_k.svg())