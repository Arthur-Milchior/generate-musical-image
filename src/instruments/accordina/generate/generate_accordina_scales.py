"""Generates, for every practiced scale pattern, SVGs of that scale over one and two octaves starting from 3
different button positions, plus an Anki notes CSV (`accordina_scale.csv`). Unlike the other `generate_*`
modules, the actual work happens inside `generate()` rather than at import time; see the note on that function
below about it currently not being called anywhere."""
from typing import List
from instruments.accordina.accordina_note import AccordinaNote
from instruments.accordina.set_of_accordina_notes import SetOfAccordinaNote
from utils.util import img_tag, save_file
from .accordina_constants import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.scale.scale_patterns import scale_patterns_I_practice

class SetOfAccordinaNoteForScale(SetOfAccordinaNote):
    """A `SetOfAccordinaNote` for one rendering of one scale (a specific pattern, starting note and number of
    octaves), used to give the generated SVG a scale-specific file name."""

    def __init__(self, notes: List[AccordinaNote], scale: ScalePattern, number_of_octaves: int):
        """`notes` are the scale's notes to highlight; `scale` and `number_of_octaves` are kept only to build
        the file name in `_svg_name_base`."""
        self.scale = scale
        """The `ScalePattern` being pictured, used to name the file after it."""
        super().__init__(notes)
        self.number_of_octaves = number_of_octaves
        """How many octaves this rendering spans (1 or 2), used to name the file."""

    def _svg_name_base(self, **kwargs) -> str:
        """Name the file after the scale, starting button position, and octave span.

        Note: reads `self.number_of_octave` (no trailing `s`), which this class never sets (only
        `self.number_of_octaves` is set in `__init__`) — calling this currently raises `AttributeError`."""
        low_note = self.notes[0]
        return f"""accordina_{self.scale.first_of_the_names()}_position_{low_note.value}_{"one_octave" if self.number_of_octave == 1 else "two_octaves"}"""



def generate():
    """Render every practiced scale (see `scale_patterns_I_practice`) at 1 and 2 octaves from 3 starting
    button positions, and write the resulting Anki notes CSV.

    Note: this function is defined but not invoked anywhere in this module or by its importers (`generate.py`
    only imports the module, it never calls `generate_accordina_scales.generate()`), and
    `SetOfAccordinaNoteForScale(notes)` below is missing the required `scale`/`number_of_octaves` arguments —
    so, as currently written, scale generation does not actually run."""
    scales_folder = f"{accordina_folder}/scales"
    ensure_folder(scales_folder)
    anki_scale_notes = []
    for pattern in scale_patterns_I_practice:
        pattern_name = pattern.first_of_the_names(True)
        anki_note =[img_tag("accordina.png"), pattern_name]
        for number_of_octave in [1, 2]:
            for low_note in [AccordinaNote(0), AccordinaNote(1), AccordinaNote(2),]:
                scale = pattern.from_note(low_note, number_of_octaves=number_of_octave)
                notes = scale.notes
                set = SetOfAccordinaNoteForScale(notes)
                file_name = set.save_svg(scales_folder)
                anki_note.append(img_tag(file_name))
        anki_scale_notes.append(",".join(anki_note))
    anki_file_path = f"""{accordina_folder}/accordina_scale.csv"""
    save_file(anki_file_path, "\n".join(anki_scale_notes))
