import unittest

from accordina.set_of_notes import SetOfAccordinaNote
from accordina.test_note import *
from .note import *

class TestSetOfAccordinaNote(unittest.TestCase):
    set_c_dsharp = SetOfAccordinaNote({C4, D4_sharp})

    def test(self):
        self.assertEqual(self.set_c_dsharp.number_of_rows(), 3)
        self.assertEqual(self.set_c_dsharp._min_note(), C4)
        self.assertEqual(self.set_c_dsharp._max_note(), D4_sharp)
        self.assertEqual(set(self.set_c_dsharp.pictured_notes()), {C4, AccordinaNote(1, selected=False), AccordinaNote(2, selected=False), D4_sharp})