import unittest

from instruments.saxophone.fingering import fingerings

from instruments.saxophone.fingering import cn
from instruments.saxophone.fingering.cn import cn_silent
from instruments.saxophone.fingering import k
from instruments.saxophone.fingering.k import k_silent
from instruments.saxophone.fingering.main_column import silent
from instruments.saxophone.fingering.fingering import *
from instruments.saxophone.fingering import rascher
from instruments.saxophone.fingering.overtone import overtone


class TestFingerings(unittest.TestCase):

    def test_e6(self):
        ordered_fingerings = list(fingerings.e6)
        expected_fingerings = [cn.e6_k, overtone.e6_A, cn.e6_t, main_column.e6_d]
        self.assertEqual(ordered_fingerings, expected_fingerings)
        expect_e6_k = Fingering.make("e6", {jay_H1, jay_H2, octave, jay_k4}, test=True)
        self.assertEqual(expect_e6_k, cn.e6_k)
        print(cn.e6_k.svg())