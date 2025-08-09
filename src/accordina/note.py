from math import sqrt
from typing import Optional
from solfege.note.chromatic import ChromaticNote
from solfege.interval.chromatic import ChromaticInterval
import unittest

radius = 7
button_distance = 20
x_distance_between_columns = int(sqrt(3)* button_distance / 2)
y_distance_between_rows = button_distance / 2
margin = x_distance_between_columns

def x(column: int) -> int:
    return x_distance_between_columns * (2-column) + margin

def y(row: int, column:int =0) -> int:
    """The center of the y coordinator of the button at row `row`. Row 0 is C4, row 1 is C#4, row 2 is D4 and D#4..."""
    return y_distance_between_rows * row + margin

class AccordinaNote(ChromaticNote):
    """
    selected: whether the note should be displayed as selected.
    absolute: whether the note represents an absolute place on the instrument, and thus should be shown is black or white if not selected
    """
    def __init__(self, *args, selected: bool=True, absolute=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = selected
        self.absolute = absolute

    def _nunber_of_semitone_from_c(self):
        return self.value

    def _column(self):
        return self._nunber_of_semitone_from_c() % 3
    
    def _diagonal_number(self):
        return self._nunber_of_semitone_from_c() // 3

    def _row(self):
        return self._column() + 2* self._diagonal_number()
    
    def fill_color(self):
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
        if self.absolute:
            if self.selected:
                return "red"
            else:
                return "black"
        else:
            return "black"
        

    
    def __eq__(self, other):
        return isinstance(other, AccordinaNote) and super().__eq__(other) and self.selected == other.selected

    def __hash__(self):
        return hash((super().__hash__(), self.selected))

    def svg(self, min_note: Optional['AccordinaNote'] = None):
        """Draw this position. The highest note pictured is `min_note`."""
        row = self._row() - min_note._row() if min_note else self ._row()
        return f"""<circle cx="{x(self._column())}" cy="{y(row, self._column())}" r="{radius}" fill="{self.fill_color()}" stroke="{self.stroke_color()}" stroke-width="2"/><!--{self.get_full_name()}-->"""
    
accordina_lowest_note = AccordinaNote(-5, selected = False, absolute=True) #G3
accordina_highest_note = AccordinaNote(accordina_lowest_note.value + 12*3, selected = False, absolute=True) #G6
