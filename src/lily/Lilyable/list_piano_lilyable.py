import unittest
from dataclasses import dataclass
from typing import List, Optional

from lily.Lilyable.piano_lilyable import PianoLilyable, TestPianoLilyable, LiteralPianoLilyable


@dataclass(eq=False)
class ListPianoLilyable(PianoLilyable):
    """Each element must have the same set of left/right/annotation"""
    list: List[PianoLilyable]
    """Separator between elements in the scale/annotation"""
    separator: str = " "

    def first_key(self) -> str:
        return self.list[0].first_key()

    def left_lily(self) -> Optional[str]:
        lefts = []
        last_key = self.first_key()
        none_found = False
        for piano_lilyable in self.list:
            lily = piano_lilyable.left_lily()
            if lily is None:
                none_found = True
                continue
            piano_lilyable_key = piano_lilyable.first_key()
            if piano_lilyable_key != last_key:
                last_key = piano_lilyable_key
                lefts.append(f"\\key {piano_lilyable_key} \major")
            lefts.append(lily)
        assert (not none_found) or (lefts == [])
        return self.separator.join(lefts)

    def right_lily(self) -> Optional[str]:
        rights = []
        last_key = self.first_key()
        none_found = False
        for piano_lilyable in self.list:
            lily = piano_lilyable.right_lily()
            if lily is None:
                none_found = True
                continue
            piano_lilyable_key = piano_lilyable.first_key()
            if piano_lilyable_key != last_key:
                last_key = piano_lilyable_key
                rights.append(f"\\key {piano_lilyable_key} \major")
            rights.append(lily)
        assert (not none_found) or (rights == [])
        return self.separator.join(rights)

    def annotations_lily(self) -> Optional[str]:
        annotations = [piano_lilyable.annotations_lily() for piano_lilyable in self.list]
        count = len([left for left in annotations if left is not None])
        if count == 0:
            return None
        assert count == len(self.list)
        return self.separator.join(annotations)


class TestList(unittest.TestCase):
    maxDiff = None
    value = ListPianoLilyable(
        [
            TestPianoLilyable.value,
            LiteralPianoLilyable("aes", "gauche", "droit", "am"),
            LiteralPianoLilyable("c", "izquierda", "derecha", "b"),
        ],
        separator="\n"
    )

    def test_lily(self):
        lily = self.value.lily()
        self.assertEquals(r"""\version "2.20.0"
\score{
  <<
    \new Lyrics {
      \lyricmode{
        IV
        am
        b
      }
    }
    \new PianoStaff<<
      \new Staff{
        \set Staff.printKeyCancellation = ##f
        \clef treble
        \key aes \major
        gis'
        droit
        \key c \major
        derecha
      }
      \new Staff{
        \set Staff.printKeyCancellation = ##f
        \clef bass
        \key aes \major
        cis
        gauche
        \key c \major
        izquierda
      }
    >>
  >>
}""", lily)
        self.assertEquals(self.value.first_key(), "aes")
        self.assertEquals(self.value.right_lily(), """gis'
droit
\key c \major
derecha""")
        self.assertEquals(self.value.left_lily(), """cis
gauche
\key c \major
izquierda""")
        self.assertEquals(self.value.annotations_lily(), """IV
am
b""")

    def test_eq(self):
        expected = LiteralPianoLilyable("aes", """cis
gauche
\\key c \major
izquierda""", """gis'
droit
\\key c \major
derecha""", """IV
am
b""")
        print(expected)
        print(self.value)
        self.assertEquals(self.value, expected)
