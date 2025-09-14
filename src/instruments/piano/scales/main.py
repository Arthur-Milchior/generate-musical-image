from utils import util
from instruments.piano.scales.generate import generate_scores
import solfege.scale.scale_pattern #Ensure that the arpeggios are generated from the scales
from consts import generate_root_folder


folder_path = f"{generate_root_folder}/piano/scales"
util.ensure_folder(folder_path)
generate_scores(folder_path=folder_path, execute_lily=True, wav=True)
