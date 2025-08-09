from typing import Generator, List, Set
from accordina.note import *
from solfege.interval.chromatic import ChromaticInterval

width = 2 * margin + 2 * x_distance_between_columns

class SetOfAccordinaNote():
    """
    absolute -- whether this represents absolute notes
    """

    def __init__(self, notes: List[AccordinaNote], absolute=False):
        self.notes = sorted(list(notes))
        self.absolute = absolute
    
    def number_of_rows(self):
        return self._max_note()._row() - self._min_note()._row() + 1

    def height(self):
        """The height of the generated svg"""
        return (self.number_of_rows()-1) * y_distance_between_rows + 2* margin
    
    def _min_note(self) -> AccordinaNote:
        return self.notes[0]

    def _max_note(self) -> AccordinaNote:
        return self.notes[-1]

    def pictured_notes(self) -> Generator[AccordinaNote]:
        for i in range (len(self.notes) - 1):
            note = self.notes[i]
            next_selected_noted = self.notes[i+1]
            while note.value != next_selected_noted.value:
                yield note
                note = AccordinaNote(note.value + 1, selected=False, absolute=self.absolute)
                
        yield self.notes[-1]

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, selected={self.selected})"

    def svg(self):
        min_note = self._min_note()
        return (f"""\
<svg version="1.1" width="{width}" height="{self.height()}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="white" />
  """ +
"\n  ".join(note.svg(min_note) for note in self.pictured_notes())
+
"""
</svg>""")