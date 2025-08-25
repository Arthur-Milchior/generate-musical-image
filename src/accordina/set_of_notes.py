from typing import Generator, List, Set
from accordina.note import *
from solfege.interval.chromatic_interval import ChromaticInterval

width = 2 * margin + 2 * x_distance_between_columns

class SetOfAccordinaNote():
    """
    absolute -- whether this represents absolute notes
    """

    def __init__(self, notes: List[AccordinaNote], min:Optional[AccordinaNote] = None, max:Optional[AccordinaNote] = None, absolute=False):
        self.notes = sorted(note.copy(selected=True, absolute=absolute) for note in notes)
        self.absolute = absolute
        self.min = min if min is not None else self._min_pictured_note()
        self.max = max if max is not None else self._max_pictured_note()
    
    def number_of_rows(self):
        return self.max._row() - self.min._row() + 1

    def height(self):
        """The height of the generated svg"""
        return (self.number_of_rows()-1) * y_distance_between_rows + 2* margin
    
    def _min_pictured_note(self) -> AccordinaNote:
        return self.notes[0].first_note_of_diagonal()

    def _max_pictured_note(self) -> AccordinaNote:
        return self.notes[-1].last_note_of_diagonal()

    def pictured_notes(self) -> Generator[AccordinaNote]:
        current_note = self.min
        next_note_index = 0
        while current_note <= self.max:
            if next_note_index < len(self.notes) and current_note.value == self.notes[next_note_index].value:
                yield self.notes[next_note_index]
                next_note_index += 1
            else:
                yield current_note
            current_note += ChromaticInterval(1)
                
        yield self.notes[-1]

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, selected={self.selected})"

    def svg(self):
        return (f"""\
<svg version="1.1" width="{width}" height="{self.height()}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="white" />
  """ +
"\n  ".join(note.svg(self.min) for note in self.pictured_notes())
+
"""
</svg>""")