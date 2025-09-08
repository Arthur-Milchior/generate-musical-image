from dataclasses import dataclass
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set.set_of_guitar_positions import SetOfGuitarPositions
from solfege.pattern.pattern import SolfegePattern
from guitar.scale.utils import scale2Pos, increase_fret_limit, decreasing_fret_limit
from utils.csv import CsvGenerator
from utils.util import *
from solfege.pattern.scale.scale_pattern import ScalePattern
import guitar.util
from consts import generate_root_folder


scale_transposable_folder = f"{generate_root_folder}/guitar/scale/transposable"
ensure_folder(scale_transposable_folder)


@dataclass(frozen=True)
class AnkiNote(CsvGenerator):
    scale: SolfegePattern


    def csv_content(self) -> List[str]:
        l = []
        return l


for scale in ScalePattern.all_patterns:
    scale_name = scale.first_of_the_names()
    intervals = scale.absolute_intervals()
    folder_scale = f"{imageFolder}/{scale_name}"
    ensure_folder(folder_scale)
    web = """<html><head><title>All transposable {scale_name} on a standard guitar</title></head><body>Each transposable version of the scale {scale_name}.<br/> Successive note are separated by {str(intervals)} half-note
<hr/>"""
    for string in range(1, 7):
        for fret in range(1, 5):
            basePos = GuitarPosition(string, fret)
            poss = scale2Pos(intervals, basePos)
            if poss is False:
                print("poss is false:continue")
                continue
            file = "%d-%d-%s.svg" % (string, fret, scale_name)
            path = "%s/%s" % (folder_scale, file)
            sop = SetOfGuitarPositions(poss)
            if not sop.is_lowest_fret_one():
                print("no fret one:continue")
                continue
            with open(path, "w") as f:
                sop.draw(f)
            web += img_tag(file) + "\n""" % file
    web += """</body></html>"""
    index += """<li><a href="%s">""" % scale_name
    for scale_name in scale.get_names():
        index += "%s, " % scale_name
    index += """</a></li>"""
    save_file("%s/index.html" % folder_scale, web)

index += """</ul></body>
</html>"""
save_file(imageFolder + "/index.html", index)
