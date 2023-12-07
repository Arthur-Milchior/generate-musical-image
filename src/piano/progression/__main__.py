from piano.progression.generate import progressions
from utils.util import ensure_folder

if __name__ == '__main__':
    folder_path = "../../../generated/piano/progressions"
    ensure_folder(folder_path)
    notes_csv = progressions(folder_path, False)
    with open(f"{folder_path}/anki.csv", "w") as f:
        f.write("\n".join(notes_csv))
