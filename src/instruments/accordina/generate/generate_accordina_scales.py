from typing import List
from instruments.accordina.accordina_note import AccordinaNote
from instruments.accordina.set_of_accordina_notes import SetOfAccordinaNote
from utils.util import img_tag, save_file
from .accordina_constants import *
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern.scale.scale_patterns import scale_patterns_I_practice

class SetOfAccordinaNoteForScale(SetOfAccordinaNote):

    def __init__(self, notes: List[AccordinaNote], scale: ScalePattern, number_of_octaves: int):
        self.scale = scale
        super().__init__(notes)
        self.number_of_octaves = number_of_octaves

    def _svg_name_base(self) -> str:
        low_note = self.notes[0]
        return f"""accordina_{self.scale.first_of_the_names()}_position_{low_note.value}_{"one_octave" if self.number_of_octave == 1 else "two_octaves"}"""



def generate():
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
