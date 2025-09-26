#from instruments.saxophone.fingering.fingering import value_to_fingering
from instruments.saxophone.fingering.saxophone_fingerings import value_to_fingerings
from consts import generate_root_folder
from utils.util import ensure_folder, img_tag, save_file
from instruments.saxophone.fingering import saxophone_fingerings

folder = f"{generate_root_folder}/saxophone"
ensure_folder(folder)

max_number_of_fingering = max(len(fingerings) for fingerings in value_to_fingerings.values())

anki_notes = []
notes = list(value_to_fingerings.keys())
notes.sort()
for value in notes:
    saxophone_fingerings = value_to_fingerings[value]
    name = saxophone_fingerings.get_name_with_octave()
    anki_note = ["saxophone", name]
    for entry, fingering in enumerate(saxophone_fingerings):
        anki_field = f"""{img_tag(fingering.save_svg(folder_path=folder, entry=entry))}/>{fingering.anki_comment()}"""
        anki_note.append(anki_field)
    while len(anki_note) <= max_number_of_fingering:
        anki_note.append("")
    anki_notes.append(",".join(anki_note))

csv_path = f"{folder}/saxophone.csv"
save_file(csv_path, "\n".join(anki_notes))