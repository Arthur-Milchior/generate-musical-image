import unittest
from accordina.note import *

half_tone = ChromaticInterval(1)
C4 = AccordinaNote(0, selected=False)
C4_sharp = C4 + half_tone
D4 = C4_sharp + half_tone
D4_sharp = D4 + half_tone
E4 = D4_sharp + half_tone
F4 = E4 + half_tone
C5 = C4 + ChromaticInterval(12)

class TestAccordinaNote(unittest.TestCase):

    def test_column(self):
        self.assertEqual(C4._column(), 0)
        self.assertEqual(C4_sharp._column(), 1)
        self.assertEqual(D4._column(), 2)
        self.assertEqual(D4_sharp._column(), 0)
        self.assertEqual(C5._column(), 0)

    def test_diagonal_number(self):
        self.assertEqual(C4._diagonal_number(), 0)
        self.assertEqual(C4_sharp._diagonal_number(), 0)
        self.assertEqual(D4._diagonal_number(), 0)
        self.assertEqual(D4_sharp._diagonal_number(), 1)
        self.assertEqual(C5._diagonal_number(), 4)

    def test_first_diagonal(self):
        self.assertEqual(C4.first_note_of_diagonal(), C4)
        self.assertEqual(C4_sharp.first_note_of_diagonal(), C4)
        self.assertEqual(D4.first_note_of_diagonal(), C4)
        self.assertEqual(D4_sharp.first_note_of_diagonal(), D4_sharp)
        self.assertEqual(E4.first_note_of_diagonal(), D4_sharp)

    def test_last_diagonal(self):
        self.assertEqual(C4.last_note_of_diagonal(), D4)
        self.assertEqual(C4_sharp.last_note_of_diagonal(), D4)
        self.assertEqual(D4.last_note_of_diagonal(), D4)
        self.assertEqual(D4_sharp.last_note_of_diagonal(), F4)
        self.assertEqual(E4.last_note_of_diagonal(), F4)

    def test_row(self):
        self.assertEqual(C4._row(), 0)
        self.assertEqual(C4_sharp._row(), 1)
        self.assertEqual(D4._row(), 2)
        self.assertEqual(D4_sharp._row(), 2)
        self.assertEqual(C5._row(), 8)

    # def test_x(self):
    #     self.assertEqual(C4.x(), 100)
    #     self.assertEqual(C4_sharp.x(), 200)
    #     self.assertEqual(D4.x(), 300)
    #     self.assertEqual(D4_sharp.x(), 100)
    #     self.assertEqual(C5.x(), 100)

    # def test_y(self):
    #     self.assertEqual(C4.y(), 100)
    #     self.assertEqual(C4_sharp.y(), 200)
    #     self.assertEqual(D4.y(), 300)
    #     self.assertEqual(D4_sharp.y(), 400)
    #     self.assertEqual(C5.y(), 500)
