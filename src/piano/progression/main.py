from piano.progression.generate import progressions
from utils.util import ensure_folder
from consts import generate_root_folder

folder_path = f"{generate_root_folder}/piano/progressions"
ensure_folder(folder_path)
notes_csv = progressions(folder_path, False)
with open(f"{folder_path}/anki.csv", "w") as f:
    f.write("\n".join(notes_csv))
