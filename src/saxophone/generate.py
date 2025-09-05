#from saxophone.fingering.fingering import value_to_fingering
from saxophone.fingering.fingerings import value_to_fingerings
from consts import generate_root_folder
from utils.util import ensure_folder
from saxophone.fingering import fingerings

folder = f"{generate_root_folder}/saxophone"
ensure_folder(folder)

max_number_of_fingering = max(len(fingerings) for fingerings in value_to_fingerings.values())

anki_notes = []
notes = list(value_to_fingerings.keys())
notes.sort()
for value in notes:
    fingerings = value_to_fingerings[value]
    name = fingerings.get_name_with_octave()
    anki_note = ["saxophone", name]
    for entry, fingering in enumerate(fingerings):
        file_name = f"saxo_{name}_{entry}.svg"
        path = f"{folder}/{file_name}"
        anki_field = f"""<img src="saxo_{name}_{entry}.svg"/>{fingering.anki_comment()}"""
        anki_note.append(anki_field)
        save_file(path, fingering.svg())
    while len(anki_note) <= max_number_of_fingering:
        anki_note.append("")
    anki_notes.append(",".join(anki_note))

csv_path = f"{folder}/saxophone.csv"
save_file(csv_path, "\n".join(anki_notes))