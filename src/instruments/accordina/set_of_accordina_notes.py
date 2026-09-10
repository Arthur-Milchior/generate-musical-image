"""Defines `SetOfAccordinaNote`: a group of accordina notes (a scale, chord or interval chunk) drawn together
on the button-grid diagram, mirroring what `fretted_instrument`'s `SetOfPos` does for frets."""
from abc import abstractmethod
from typing import Generator, List, Set
from instruments.accordina.accordina_note import *
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.svg.svg_generator import SvgGenerator

width = 2 * margin + 2 * x_distance_between_columns
"""Fixed SVG width (in user units) of any accordina diagram: always 3 columns plus margins, regardless of
how many notes/rows are pictured."""

class SetOfAccordinaNote(SvgGenerator):
    """A set of notes to highlight together on the accordina's button grid (e.g. the notes of a scale or
    chord), plus enough context (`min`/`max` pictured notes) to know which unselected buttons around them
    also need to be drawn so the diagram reads as a coherent chunk of the instrument."""

    notes: List[AccordinaNote]
    """The notes to highlight (selected), sorted."""

    absolute: bool
    """Whether the notes in this set represent absolute (fixed) places on the instrument rather than
    relative positions within, e.g., a movable scale/chord shape."""

    min: AccordinaNote
    """The lowest note pictured in the diagram."""

    max: AccordinaNote
    """The highest note pictured in the diagram."""

    def __init__(self, notes: List[AccordinaNote], min:Optional[AccordinaNote] = None, max:Optional[AccordinaNote] = None, absolute: bool = False) -> None:
        """`notes` are the notes to highlight (selected); marked `absolute` if given. `min`/`max` bound the
        range of buttons pictured around them, defaulting to the full diagonals containing the lowest/highest
        of `notes` (see `_min_pictured_note`/`_max_pictured_note`)."""
        self.notes = sorted(note.copy(selected=True, absolute=absolute) for note in notes)
        self.absolute = absolute
        """Whether the notes in this set represent absolute (fixed) places on the instrument rather than
        relative positions within, e.g., a movable scale/chord shape."""
        self.min = min if min is not None else self._min_pictured_note()
        self.max = max if max is not None else self._max_pictured_note()

    def number_of_rows(self) -> int:
        """Return how many grid rows (inclusive) span from `self.min` to `self.max`."""
        return self.max._row() - self.min._row() + 1

    def _min_pictured_note(self) -> AccordinaNote:
        """Return the lowest note that must be pictured: the start of the diagonal containing the lowest note
        in `self.notes`."""
        return self.notes[0].first_note_of_diagonal()

    def _max_pictured_note(self) -> AccordinaNote:
        """Return the highest note that must be pictured: the end of the diagonal containing the highest note
        in `self.notes`."""
        return self.notes[-1].last_note_of_diagonal()

    def pictured_notes(self) -> List[AccordinaNote]:
        """Return every note between `self.min` and `self.max` (inclusive), substituting the matching entry
        from `self.notes` (selected) wherever one falls at that chromatic value, and unselected notes
        elsewhere — i.e. the full ordered list of buttons the diagram must draw."""
        current_note = self.min
        next_note_index = 0
        l = []
        while current_note <= self.max:
            if next_note_index < len(self.notes) and current_note.value == self.notes[next_note_index].value:
                l.append(self.notes[next_note_index])
                next_note_index += 1
            else:
                l.append(current_note)
            current_note += ChromaticInterval.make(1)

        l.append(self.notes[-1])
        return l

    def __repr__(self) -> str:
        """Return a `<ClassName>(value=..., selected=...)`-shaped string for debugging.

        Note: this references `self.value`/`self.selected`, which this class does not define — inherited from
        a subclass that mixes in a single note's attributes, if any; otherwise calling `repr()` here will raise."""
        return f"{self.__class__.__name__}(value={self.value}, selected={self.selected})"

    #pragma mark - SvgGenerator
    def svg_lines(self) -> List[str]:
        """The content of the svg. Not containig svg itself and the white background."""
        return [note.svg_line(self.min) for note in self.pictured_notes()]

    @abstractmethod
    def _svg_name_base(self, **kwargs) -> str:
        """Return the base file name (without extension) for the generated SVG; must be implemented by
        subclasses (e.g. to name the file after the scale/chord/interval being drawn)."""
        ...

    def svg_height(self, *args, **kwargs) -> int:
        """The height of the generated svg"""
        return (self.number_of_rows()-1) * y_distance_between_rows + 2* margin

    def svg_width(self, *args, **kwargs) -> int:
        "Returns the width of svg. Must accept same argument as svg"
        return width