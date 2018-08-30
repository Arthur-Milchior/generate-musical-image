
from guitar.util import *
import os
from util import *
from guitar.pos import Pos, SetOfPos
from solfege.scales import Scale_Pattern
import guitar.util 
leafFolder="scale/"
imageFolder=guitar.util.imageFolder+leafFolder
ankiFolder=guitar.util.ankiFolder+leafFolder

increase_fret_limit = 4
decreasing_fret_limit=4
def scale2Pos(intervals,basePos):
    poss = [basePos]
    lastPos =basePos
    firstFret = basePos.fret
    for interval in intervals:
        pos = lastPos.add(interval, min = max(lastPos.fret -4,1), max = firstFret +4)
        if pos is None:
            return False
        if pos.string != lastPos.string:
            firstFret= pos.fret
        poss.append(pos)
        lastPos = pos
    return poss

major = [2,2,1,2,2,2,1]
pos1= Pos(1,1)
index = """<html><head><title>All transposable scale on a standard guitar</title></head>
<body>
Here is the list of each scales I found in English wikipedia. With the exception of the scales which can not be easily be played on guitar, e.g. scales using interval smaller than half-tones.

For each of them, there is the list of way to play this scale, on one octave, on a standard guitar fret. The only exception being the <a href="https://en.wikipedia.org/wiki/Algerian_scale">Algerian scale</a> which, by definition, is played on two octaves.

Here are the technical restrictions I used, to choose which scale's position to generates.
<ul><li>
It is assumed that, there is never more than %d fret from the first to the last note played on a single string.
</li><li> Furthermore, there is never more than %d fret in distance from the the highest note played on a string, and the lowest note played on the following string. </li></lu>
<ul>
"""%(increase_fret_limit,decreasing_fret_limit)

for scale in Scale_Pattern.set_[Scale_Pattern]:
    name = scale.getFirstName()
    intervals=scale.getIntervals()
    folder_scale = imageFolder+name
    ensureFolder(folder_scale)
    web = """<html><head><title>All transposable %s on a standard guitar</title></head><body>Each transposable version of the scale %s.<br/> Successive notes are separated by %s half-notes
<hr/>"""%(name,name, str(intervals))
    for string in range(1,7):
        for fret in range(1,5):
            print ("""considering %s %d-%d"""%(name,string,fret))
            basePos = Pos(string,fret)
            poss = scale2Pos(intervals, basePos)
            if poss is False:
                print("poss is false:continue")
                continue
            file ="%d-%d-%s.svg"%( string, fret, name)
            path = "%s/%s" %(  folder_scale,file)
            sop=SetOfPos(poss)
            debug(sop)
            if not sop.isOneMin():
                print("no fret one:continue")
                continue
            debug("drawing")
            with open (path, "w") as f:
                sop.draw(f)
            web += """<img src="%s"/>\n"""%file
    web+="""</body></html>"""
    index += """<li><a href="%s">"""%name
    for name in scale.getNames():
        index += "%s, " % name
    index +="""</a></li>"""
    with open("%s/index.html"% folder_scale,"w") as f:
        f.write(web)



index +="""</ul></body>
</html>"""
with open(imageFolder+"/index.html","w") as f:
    f.write(index)
