import unittest
from .note import *

C4 = AccordinaNote(0)
C4_sharp = AccordinaNote(1)
D4 = AccordinaNote(2)
D4_sharp = AccordinaNote(3)
C5 = AccordinaNote(12)

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
