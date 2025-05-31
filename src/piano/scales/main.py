from utils import util
from .generate import generate_scores
import solfege.scale.scale_pattern #Ensure that the arpeggios are generated from the scales


folder_path = "../../generated/piano/scales"
util.ensure_folder(folder_path)
generate_scores(folder_path=folder_path, execute_lily=True, wav=True)
