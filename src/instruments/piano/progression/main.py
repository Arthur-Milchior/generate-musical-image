"""Generation script for `python3 -m instruments.piano.progression` (via `__main__.py`): renders every chord
progression in `progressions_in_C.py` in every key and writes the corresponding Anki notes CSV.

Currently non-functional: `generate.py`, `chord_progression.py`, `pattern.py` and `progressions_in_C.py` are
entirely commented out (work in progress), so `progressions` does not exist and this import fails."""
from instruments.piano.progression.generate import progressions
from utils.util import ensure_folder
from consts import generate_root_folder

folder_path = f"{generate_root_folder}/piano/progressions"
ensure_folder(folder_path)
notes_csv = progressions(folder_path, False)
save_file(f"{folder_path}/anki.csv", "\n".join(notes_csv))
