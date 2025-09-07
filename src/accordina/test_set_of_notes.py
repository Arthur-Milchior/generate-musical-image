import unittest

from accordina.set_of_accordina_notes import SetOfAccordinaNote
from accordina.test_note import *
from accordina.accordina_note import *

class TestSetOfAccordinaNote(unittest.TestCase):
    set_c_dsharp = SetOfAccordinaNote({C4, D4_sharp})

    def test(self):
        self.assertEqual(self.set_c_dsharp.number_of_rows(), 5)
        self.assertEqual(self.set_c_dsharp._min_pictured_note(), C4)
        self.assertEqual(self.set_c_dsharp._max_pictured_note(), F4)
        self.assertEqual(set(self.set_c_dsharp.pictured_notes()), {AccordinaNote(0, selected=True), C4_sharp, D4, AccordinaNote(3, selected=True), E4, F4})