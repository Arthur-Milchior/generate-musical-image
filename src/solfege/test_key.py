import unittest
from solfege.key import *


class TestClef(unittest.TestCase):

    def test_enharmonic(self):
        found = set()
        for enharmonic_key in sets_of_enharmonic_keys:
            chromatic_of_first_key = enharmonic_key[0].note.get_chromatic()
            self.assertNotIn(chromatic_of_first_key, found)
            found.add(chromatic_of_first_key)
            for key in enharmonic_key:
                chromatic_of_key = key.note.get_chromatic()
                self.assertTrue(chromatic_of_first_key.equals_modulo_octave(chromatic_of_key))
            for i in range(len(enharmonic_key) - 1):
                self.assertLessEqual(enharmonic_key[i], enharmonic_key[i + 1])

    def test_simplest_major(self):
        self.assertEqual(key_of_C, key_of_C.simplest_enharmonic_major())
        self.assertEqual(key_of_C, Key(Note.from_name("D♭♭"), number_of_flats=12).simplest_enharmonic_major())

    def test_simplest_minor(self):
        self.assertEqual(key_of_A, key_of_A.simplest_enharmonic_minor())
        self.assertEqual(key_of_A, Key(Note.from_name("B♭♭3"), number_of_flats=9).simplest_enharmonic_minor())
        self.assertEqual(key_of_A, Key(Note.from_name("B♭♭"), number_of_flats=9).simplest_enharmonic_minor())

    # def test_alteration(self):
    #     self.assertEqual(enharmonic_keys[0].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[1].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[2].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[3].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[4].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[5].note.get_alteration(), IntervalMode(-1))
    #     self.assertEqual(enharmonic_keys[6].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[7].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[8].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[9].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[10].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[11].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[12].note.get_alteration(), IntervalMode(0))
    #     self.assertEqual(enharmonic_keys[13].note.get_alteration(), IntervalMode(1))
    #     self.assertEqual(enharmonic_keys[14].note.get_alteration(), IntervalMode(1))

    def test_get(self):
        self.assertEqual(key_of_C, Key.from_note(Note.from_name("C")))
