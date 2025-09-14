from instruments.piano.progression.generate import progressions
from utils.util import ensure_folder
from consts import generate_root_folder

folder_path = f"{generate_root_folder}/piano/progressions"
ensure_folder(folder_path)
notes_csv = progressions(folder_path, False)
save_file(f"{folder_path}/anki.csv", "\n".join(notes_csv))
