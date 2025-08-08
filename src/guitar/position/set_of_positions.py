from __future__ import annotations

from typing import Iterable, List, Iterator, Optional
from unittest import TestCase

from guitar.position.guitar_position import GuitarPosition, string_distance, fret_distance


def fret_svg(nb_frets: int) -> List[str]:
    """The svg for the guitar, with `nb_frets` frets"""
    assert 0 < nb_frets <= 24
    svg_lines = []
    for i in range(1, 7):
        # columns
        x = string_distance * (i - .5)
        y1 = fret_distance / 2
        y2 = fret_distance * (nb_frets + .5)
        svg_lines.append(f"""<line x1="{int(x)}" y1="{int(y1)}" x2="{int(x)}" y2="{int(y2)}" stroke-width="4" stroke="black" />""")
    for i in range(1, nb_frets + 2):
        # lines
        x1 = string_distance / 2
        x2 = string_distance * 5.5
        y = fret_distance * (i - .5)
        svg_lines.append(f"""<line x1="{int(x1)}" y1="{int(y)}" x2="{int(x2)}" y2="{int(y)}" stroke-width="4" stroke="black" />""")
    return svg_lines


class SetOfGuitarPositions:
    """
    A set of positions on the guitar.

    There may be 0, 1 or many note by strings.
    Iterated in GuitarPosition order.
    """

    """The set of positions"""
    _positions: List[GuitarPosition]

    def __init__(self, set: Optional[Iterable[GuitarPosition]] = []):
        self._positions = list(set)
        self.dic = dict()

    def get_lowest_note(self) -> Optional[GuitarPosition]:
        return min(self._positions) if self._positions else None

    def add(self, position: GuitarPosition):
        """A set similar to `self`, with `position`"""
        ret = SetOfGuitarPositions()
        ret._positions = self._positions + [position]
        return ret

    def __iter__(self) -> Iterator[GuitarPosition]:
        self._positions.sort()
        return iter(self._positions)

    def __eq__(self, other: SetOfGuitarPositions):
        return set(self._positions) == set(other._positions)

    def _max_fret(self):
        """The position of the greatest fret used. 0 when there are no note to play"""
        m = 0
        for position in self._positions:
            if position.fret is not None:
                m = max(m, position.fret)
        return m

    def svg(self, nbFretMin: int =0) -> str:
        nb_frets_needed = self._max_fret() + 1
        nb_frets = max(nb_frets_needed, nbFretMin)
        height = (nb_frets * fret_distance)
        width = string_distance * 6
        new_line = "\n"
        return f"""\
<svg xmlns="http://www.w3.org/2000/svg" width="{int(width)}" height="{int(height)}" version="1.1">
{f"{new_line}  ".join([position.svg() for position in self] + fret_svg(nb_frets))}
</svg>"""
    
    def is_included_in(self, other: SetOfGuitarPositions):
        return set(self._positions) <= set(other._positions)


class TestSetOfGuitarPositions(TestCase):
    def test_eq(self):
        self.assertEqual(SetOfGuitarPositions(), SetOfGuitarPositions())
        self.assertNotEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1)),
                             SetOfGuitarPositions().add(GuitarPosition(string=1, fret=2)))
        self.assertNotEqual(SetOfGuitarPositions(),
                             SetOfGuitarPositions().add(GuitarPosition(string=1, fret=2)))
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1)),
                          SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1)))
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1)),
                          SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1))
                          .add(GuitarPosition(string=1, fret=1)))
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1)),
                          SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1))
                          .add(GuitarPosition(string=1, fret=2)))

    def test_iter(self):
        self.assertEqual(list(SetOfGuitarPositions()),
                          [])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1))),
                          [GuitarPosition(string=1, fret=1)])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1))
                               .add(GuitarPosition(string=2, fret=2))),
                          [GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=2)])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(string=2, fret=2))
                               .add(GuitarPosition(string=1, fret=1))),
                          [GuitarPosition(string=1, fret=1), GuitarPosition(string=2, fret=2)])

    def test_max_fret(self):
        self.assertEqual(SetOfGuitarPositions()._max_fret(), None)
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=None))._max_fret(), None)
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(string=1, fret=1))._max_fret(), 1)
