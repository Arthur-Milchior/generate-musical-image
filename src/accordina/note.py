from dataclasses import dataclass
from math import sqrt
from typing import Optional
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.note.note import Note

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

@dataclass(frozen=True)
class AccordinaNote(ChromaticNote):
    """
    whether the note should be displayed as selected.
    """
    selected: bool
    """
    whether the note represents an absolute place on the instrument, and thus should be shown is black or white if not selected
    """
    absolute: bool = False

    def __repr__(self):
        return f"""AccordinaNote(value={self.value}, selected={self.selected}, absolute={self.absolute})"""

    def _nunber_of_semitone_from_c(self):
        return self.value

    def make_instance_of_selfs_class(self, value: int):
        return AccordinaNote(value, selected=self.selected, absolute = self.absolute)

    def _column(self):
        return self._nunber_of_semitone_from_c() % 3
    
    def _diagonal_number(self):
        return self._nunber_of_semitone_from_c() // 3

    def _row(self):
        return self._column() + 2* self._diagonal_number()
    
    def first_note_of_diagonal(self):
        return max(self - ChromaticInterval(self._column()), min_accordina_note).copy(selected=False)

    def last_note_of_diagonal(self):
        return min(self + ChromaticInterval(2 - self._column()), max_accordina_note).copy(selected=False)
    
    def copy(self, selected: Optional[bool] = None, absolute: Optional[bool] = None):
        return AccordinaNote(value = self.value,
                              selected=selected if selected is not None else self.selected,
                              absolute=absolute if absolute is not None else self.absolute
                              )

    def _add(self, other):
        note = super()._add(other)
        return AccordinaNote(note.value, selected=self.selected, absolute = self.absolute)
    
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
        return f"""<circle cx="{x(self._column())}" cy="{y(row, self._column())}" r="{radius}" fill="{self.fill_color()}" stroke="{self.stroke_color()}" stroke-width="2"/><!--{self.get_name_with_octave()}-->"""
    
accordina_lowest_note = AccordinaNote(-5, selected = False, absolute=True) #G3
accordina_highest_note = AccordinaNote(accordina_lowest_note.value + 12*3, selected = False, absolute=True) #G6

min_accordina_note = AccordinaNote(Note.from_name("G3").get_chromatic().value, selected=False, absolute=True)
max_accordina_note = AccordinaNote(Note.from_name("G6").get_chromatic().value, selected=False, absolute=True)
