from fileinput import filename
from instruments.accordina.set_of_accordina_notes import SetOfAccordinaNote
from utils.util import img_tag, save_file
from .accordina_constants import *
from instruments.accordina.accordina_note import *


notes_folder = f"{accordina_folder}/notes"
ensure_folder(notes_folder)
anki_fingering_notes = []
for value in range(accordina_lowest_note.value, accordina_highest_note.value+1):
    fingered_note = AccordinaNote(value, absolute=True)
    set = SetOfAccordinaNote({fingered_note}, absolute= True, min=min_accordina_note, max=max_accordina_note)
    svg_name = f"accordina_{value}.svg"
    svg = set.svg()
    path = f"{notes_folder}/{svg_name}"
    degree = fingered_note.get_degree()
    alteration = "♭" if "♭" in degree else ("#" if "#" in degree else "")
    save_file(path, svg)
    anki_fingering = [
        "Accordina",
        degree,#degree
        alteration, #alteration
        str(fingered_note.octave(scientific_notation=True)), #octave
        "", # function
        img_tag(filename)
        ]
    anki_fingering_notes.append(",".join(anki_fingering))

anki_file_path = f"""{accordina_folder}/accordina_fingering.csv"""
save_file(anki_file_path, "\n".join(anki_fingering_notes))