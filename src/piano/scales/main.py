from utils import util
from .generate import generate_scores

folder_path = "../../generated/piano/scales"
util.ensure_folder(folder_path)
generate_scores(folder_path=folder_path, execute_lily=True, wav=True)
