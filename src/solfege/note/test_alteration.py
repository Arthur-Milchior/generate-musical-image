import unittest

from src.solfege.note.alteration import Alteration


class TestAlterationNote(unittest.TestCase):
    def test_from_name(self):
        self.assertEqual(Alteration.from_name("𝄪"), Alteration(2))
        self.assertEqual(Alteration.from_name("#"), Alteration(1))
        with self.assertRaises(Exception):
            self.assertEqual(Alteration.from_name("###"), Alteration(1))
