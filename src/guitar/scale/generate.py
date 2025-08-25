from dataclasses import dataclass
from guitar.position.guitar_position import GuitarPosition
from guitar.position.set_of_guitar_positions import SetOfGuitarPositions
from solfege.solfege_pattern import SolfegePattern
from guitar.scale.utils import scale2Pos, increase_fret_limit, decreasing_fret_limit
from utils.util import *
from solfege.scale.scale_pattern import ScalePattern
import guitar.util

leafFolder = "scale/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder

index = f"""<html><head><title>All transposable scale on a standard guitar</title></head>
<body>
Here is the list of each scales I found in English wikipedia. With the exception of the scales which can not be easily be played on guitar, e.g. scales using interval smaller than half-tones.

For each of them, there is the list of way to play this scale, on one octave, on a standard guitar fret. The only exception being the <a href="https://en.wikipedia.org/wiki/Algerian_scale">Algerian scale</a> which, by definition, is played on two octaves.

Here are the technical restrictions I used, to choose which scale's position to generates.
<ul><li>
It is assumed that, there is never more than {increase_fret_limit} fret from the first to the last note played on a single string.
</li><li> Furthermore, there is never more than {decreasing_fret_limit} fret in distance from the the highest note played on a string, and the lowest note played on the following string. </li></lu>
<ul>
"""

@dataclass(frozen=True)
class AnkiNote:
    scale: SolfegePattern


for scale in ScalePattern.class_to_patterns[ScalePattern]:
    name = scale.first_of_the_names()
    intervals = scale.get_intervals()
    folder_scale = imageFolder + name
    ensure_folder(folder_scale)
    web = """<html><head><title>All transposable %s on a standard guitar</title></head><body>Each transposable version of the scale %s.<br/> Successive note are separated by %s half-note
<hr/>""" % (name, name, str(intervals))
    for string in range(1, 7):
        for fret in range(1, 5):
            print("""considering %s %d-%d""" % (name, string, fret))
            basePos = GuitarPosition(string, fret)
            poss = scale2Pos(intervals, basePos)
            if poss is False:
                print("poss is false:continue")
                continue
            file = "%d-%d-%s.svg" % (string, fret, name)
            path = "%s/%s" % (folder_scale, file)
            sop = SetOfGuitarPositions(poss)
            if not sop.is_lowest_fret_one():
                print("no fret one:continue")
                continue
            with open(path, "w") as f:
                sop.draw(f)
            web += """<img src="%s"/>\n""" % file
    web += """</body></html>"""
    index += """<li><a href="%s">""" % name
    for name in scale.get_names():
        index += "%s, " % name
    index += """</a></li>"""
    with open("%s/index.html" % folder_scale, "w") as f:
        f.write(web)

index += """</ul></body>
</html>"""
with open(imageFolder + "/index.html", "w") as f:
    f.write(index)
