from solfege.interval.chromatic import ChromaticInterval
from guitar.position.guitar_position import GuitarPosition
from solfege.note import ChromaticNote
import unittest


class TestGuitarPosition(unittest.TestCase):
  
  # The first string played open
  openFirstString = GuitarPosition(1, 0)
  # The first string played on the first fret
  one = GuitarPosition(1,1)

  def test_open_string(self):
    self.assertEqual (repr(self.openFirstString), "GuitarPosition(string=1, fret=0)")
    self.assertEqual(self.openFirstString.svg(),"""
    <circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
    self.assertEqual(self.openFirstString.get_chromatic(), ChromaticNote(-8))

  def test_close_string(self):
    self.assertEqual (repr(self.one),"GuitarPosition(string=1, fret=1)")
    self.assertEqual(self.one.svg(),"""
    <circle cx="15" cy="50" r="11" fill="black" stroke="black" stroke-width="3"/>""")

  def test_minus(self):
    self.assertEqual (self.one.get_chromatic() , ChromaticNote(-7))
    self.assertEqual (self.one-self.openFirstString , ChromaticInterval(1))
    self.assertEqual (self.openFirstString-self.one , ChromaticInterval(-1))
    self.assertEqual (self.one-self.one , ChromaticInterval(0))

  def test_add(self):
    self.assertEqual (self.openFirstString+(ChromaticInterval(1)), self.one)
    self.assertEqual (self.openFirstString+(ChromaticInterval(4)), GuitarPosition(1,4))
    self.assertEqual (self.openFirstString+(ChromaticInterval(6)), GuitarPosition(2,1))

  def test_sop(self):
    self.assertEqual(self.one.toSop().svg(),"""\
    <svg xmlns="http://www.w3.org/2000/svg" width="180" height="100" version="1.1">
      <line x1="15" y1="25" x2="15" y2="75" stroke-width="4" stroke="black" />
      <line x1="45" y1="25" x2="45" y2="75" stroke-width="4" stroke="black" />
      <line x1="75" y1="25" x2="75" y2="75" stroke-width="4" stroke="black" />
      <line x1="105" y1="25" x2="105" y2="75" stroke-width="4" stroke="black" />
      <line x1="135" y1="25" x2="135" y2="75" stroke-width="4" stroke="black" />
      <line x1="165" y1="25" x2="165" y2="75" stroke-width="4" stroke="black" />
      <line x1="15" y1="25" x2="165" y2="25" stroke-width="4" stroke="black" />
      <line x1="15" y1="75" x2="165" y2="75" stroke-width="4" stroke="black" />
      <circle cx="15" cy="50" r="11" fill="black" stroke="black" stroke-width="3"/>
    </svg>""")
