"""Defines `AccordinaNote`: a note positioned on the accordina's diagonal button grid, plus the pure geometry
functions (`x`, `y`) shared with `set_of_accordina_notes.py` to place a button in the generated SVG.

The accordina's buttons are arranged in 3 columns of diagonally-offset rows, one semitone apart along each
diagonal: `_column`/`_diagonal_number`/`_row` derive a note's grid position from its chromatic `value`."""
from dataclasses import dataclass
from math import sqrt
from typing import Optional
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.note import Note
from utils.svg.svg_line import SvgLine

radius = 7
"""Radius (in SVG user units) of a single button circle."""

button_distance = 20
"""Distance between the centers of two vertically-adjacent buttons in the same column."""

x_distance_between_columns = int(sqrt(3)* button_distance / 2)
"""Horizontal distance between two adjacent columns, derived from `button_distance` so buttons are packed
hexagonally (each button touches its diagonal neighbors)."""

y_distance_between_rows = button_distance / 2
"""Vertical distance between two consecutive rows (each row is a semitone higher than the previous)."""

margin = x_distance_between_columns
"""Blank margin left around the grid so buttons at the edge aren't clipped by the SVG canvas."""

def x(column: int) -> int:
    """The x coordinate of the center of a button in `column` (0, 1 or 2), columns numbered right-to-left."""
    return x_distance_between_columns * (2-column) + margin

def y(row: int, column:int =0) -> int:
    """The center of the y coordinator of the button at row `row`. Row 0 is C4, row 1 is C#4, row 2 is D4 and D#4..."""
    return y_distance_between_rows * row + margin

@dataclass(frozen=True)
class AccordinaNote(ChromaticNote, SvgLine):
    """A note on the accordina, positioned according to the instrument's diagonal button-grid geometry and
    carrying enough state (`selected`, `absolute`) to know how to draw itself as one button."""
    selected: bool
    """Whether this note should be drawn as selected/highlighted (in red) in the diagram."""

    absolute: bool = False
    """Whether this note represents a fixed, absolute place on the instrument (drawn black/white like a piano
    key when not selected) rather than a relative position within a displayed scale/chord/interval."""

    def __repr__(self):
        """Return an `AccordinaNote(...)`-shaped string for debugging."""
        return f"""AccordinaNote(value={self.value}, selected={self.selected}, absolute={self.absolute})"""

    def _nunber_of_semitone_from_c(self):
        """Return the chromatic `value`, i.e. the number of semitones from C (the grid's column/row math is
        expressed in terms of this)."""
        return self.value

    def make_instance_of_selfs_class(self, value: int):
        """Return a new `AccordinaNote` at chromatic `value`, keeping this note's `selected`/`absolute` flags
        (used by `ChromaticNote` arithmetic, e.g. `+`/`-`, to build a same-typed result)."""
        return AccordinaNote(value, selected=self.selected, absolute = self.absolute)

    def _column(self):
        """Return the grid column (0, 1 or 2) this note falls into."""
        return self._nunber_of_semitone_from_c() % 3

    def _diagonal_number(self):
        """Return the index of the diagonal (group of 3 consecutive semitones) this note belongs to."""
        return self._nunber_of_semitone_from_c() // 3

    def _row(self):
        """Return the grid row this note is drawn on, combining its column and diagonal number."""
        return self._column() + 2* self._diagonal_number()

    def first_note_of_diagonal(self):
        """Return the lowest (leftmost) note on this note's diagonal, clamped to `min_accordina_note`, as an
        unselected note (used to determine where a diagram should start drawing)."""
        return max(self - ChromaticInterval.make(self._column()), min_accordina_note).copy(selected=False)

    def last_note_of_diagonal(self):
        """Return the highest (rightmost) note on this note's diagonal, clamped to `max_accordina_note`, as an
        unselected note (used to determine where a diagram should stop drawing)."""
        return min(self + ChromaticInterval.make(2 - self._column()), max_accordina_note).copy(selected=False)

    def copy(self, selected: Optional[bool] = None, absolute: Optional[bool] = None):
        """Return a copy of this note, overriding `selected`/`absolute` where given and keeping the current
        value otherwise."""
        return AccordinaNote(value = self.value,
                              selected=selected if selected is not None else self.selected,
                              absolute=absolute if absolute is not None else self.absolute
                              )

    def fill_color(self):
        """Return this button's fill color: black/white by piano key color if `absolute`, else red if
        `selected` and white otherwise."""
        if self.absolute:
            if self.get_note().is_black_key_on_piano():
                return "black"
            else:
                return "white"
        else:
            if self.selected:
                return "red"
            else:
                return "white"

    def stroke_color(self):
        """Return this button's outline color: red if `absolute` and `selected`, black otherwise."""
        if self.absolute:
            if self.selected:
                return "red"
            else:
                return "black"
        else:
            return "black"

    def __eq__(self, other):
        """Equal if `other` is an `AccordinaNote` with the same pitch and the same `selected` state."""
        return isinstance(other, AccordinaNote) and super().__eq__(other) and self.selected == other.selected

    def __hash__(self):
        """Hash consistently with `__eq__`, combining the pitch hash with `selected`."""
        return hash((super().__hash__(), self.selected))

    def svg_line(self, min_note: Optional['AccordinaNote'] = None):
        """Return this note's SVG `<circle>`. `min_note`, if given, is the lowest note pictured in the diagram
        (used as the row-0 reference so this note's row is expressed relative to it, i.e. how far up the
        diagram it is drawn); with no `min_note`, this note's own absolute row is used."""
        row = self._row() - min_note._row() if min_note else self ._row()
        return f"""<circle cx="{x(self._column())}" cy="{y(row, self._column())}" r="{radius}" fill="{self.fill_color()}" stroke="{self.stroke_color()}" stroke-width="2"/><!--{self.get_name_with_octave()}-->"""

# The accordina's playable range, G3 to G6 (3 octaves), as `absolute` reference notes.
accordina_lowest_note = AccordinaNote(-5, selected = False, absolute=True) #G3
accordina_highest_note = AccordinaNote(accordina_lowest_note.value + 12*3, selected = False, absolute=True) #G6

min_accordina_note = AccordinaNote(Note.from_name("G3").get_chromatic().value, selected=False, absolute=True)
"""Lowest note the accordina can play (G3); used to clamp diagrams so they never try to draw below the
instrument's actual range."""

max_accordina_note = AccordinaNote(Note.from_name("G6").get_chromatic().value, selected=False, absolute=True)
"""Highest note the accordina can play (G6); used to clamp diagrams so they never try to draw above the
instrument's actual range."""
