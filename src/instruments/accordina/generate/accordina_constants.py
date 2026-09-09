"""Shared constants for the `generate/` scripts: the output folder every accordina generator writes into."""
from consts import generate_root_folder
from utils.util import ensure_folder

accordina_folder = f"{generate_root_folder}/accordina"
"""Root output folder for every generated accordina file (scales/intervals/fingerings subfolders and CSVs)."""
ensure_folder(accordina_folder)
