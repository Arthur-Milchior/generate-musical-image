from typing import Generator, List, Set
from instruments.accordina.accordina_note import *
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.svg import SvgGenerator

width = 2 * margin + 2 * x_distance_between_columns

class SetOfAccordinaNote(SvgGenerator):
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
    
    def _min_pictured_note(self) -> AccordinaNote:
        return self.notes[0].first_note_of_diagonal()

    def _max_pictured_note(self) -> AccordinaNote:
        return self.notes[-1].last_note_of_diagonal()

    def pictured_notes(self) -> List[AccordinaNote]:
        current_note = self.min
        next_note_index = 0
        l = []
        while current_note <= self.max:
            if next_note_index < len(self.notes) and current_note.value == self.notes[next_note_index].value:
                l.append(self.notes[next_note_index])
                next_note_index += 1
            else:
                l.append(current_note)
            current_note += ChromaticInterval(1)
                
        l.append(self.notes[-1])
        return l

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, selected={self.selected})"
    
    #pragma mark - SvgGenerator
    def _svg_content(self) -> List[str]:
        """The content of the svg. Not containig svg itself and the white background."""
        return [note.svg(self.min) for note in self.pictured_notes()]
    
    def _svg_name_base(self) -> str:
        return NotImplemented
    
    def svg_height(self, *args, **kwargs) -> int: 
        """The height of the generated svg"""
        return (self.number_of_rows()-1) * y_distance_between_rows + 2* margin
    
    def svg_width(self, *args, **kwargs) -> int: 
        "Returns the width of svg. Must accept same argument as svg"
        return width