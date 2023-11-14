print("Running piano")

import sys
from .fingering import *
from solfege.Scale.pattern import ScalePattern
import lily.lily
import util

leafFolder = "piano/scales/"
imageFolder = util.imageFolder + leafFolder
ankiFolder = util.ankiFolder + leafFolder

doCompile = True
root_html = """
<html><head><title>Fingerings of every scales</title></head><body>
<header><h1>Fingerings of every scales</h1></header>
<ul>
"""

anki = ""
dont_exists = []
for scale in ScalePattern.class_to_patterns[ScalePattern]:
    scaleName = scale.get_the_first_of_the_name()
    nbBemol = scale.get_number_of_bemols()
    nbSharp = scale.get_number_of_sharps()
    intervals = scale.get_intervals()
    root_html += """<li><a href='%s'>%s</a></li>""" % (scaleName, scaleName)
    scale_html = """
    <html><head><title>Fingerings of %s</title></head><body>
        <header><h1>Fingerings of %s</h1></header>
    <ul>
    """ % (scaleName, scaleName)
    folder_scale = imageFolder + "%s/" % scaleName
    util.ensureFolder(folder_scale)
    with open("""%s/anki.csv""" % folder_scale, "w") as anki_scale_file:
        for (baseNote, nbBemol_) in twelve_notes:
            baseNameTitle = baseNote.get_interval_name()
            baseNameFile = baseNote.get_interval_name("file")
            scale_html += """<li><a href='%s'>%s</a></li>""" % (baseNameFile, baseNameTitle)
            scale_note_html = """
        <html><head><title>Fingerings of %s %s</title></head><body>
        <header><h1>Fingerings of %s %s</h1></header>
        <ul>
        """ % (baseNameTitle, scaleName, baseNameTitle, scaleName)

            nbSharpFinal = nbSharp - nbBemol_
            nbBemolFinal = nbBemol + nbBemol_
            if nbSharpFinal > nbBemolFinal:
                key = ["c", "g", "d", "a", "e", "b", "fis", "cis", "gis", "dis", "ais", "eis", "bis"][nbSharpFinal]
            else:
                key = \
                ["c", "f", "bes", "ees", "aes", "des", "ges", "ces", "fes", "beses", "eeses", "aeses", "deses", "ceses",
                 "feses"][nbBemolFinal]
            debug("%s has %d bemol, %s has %d bemol and %d sharp.\nTotal is %d bemol and %d sharp.\nThe key is %s." % (
                baseNote.get_interval_name(), nbBemol_, scaleName, nbBemol, nbSharp, nbSharpFinal, nbBemolFinal, key))
            folder_scale_note = "%s%s/" % (folder_scale, baseNameFile)
            ensureFolder(folder_scale_note)
            anki += ("\n%s,%s" % (scaleName, baseNameFile))
            anki_scale_file.write("\n%s,%s" % (scaleName, baseNameFile))
            if doCompile:
                try:
                    leftFingeringDic = generate_left_fingering_dic(baseNote, intervals)
                except TooBigAlteration as tba:
                    tba.addInformation("hand", "left")
                    tba.addInformation("base note", baseNote)
                    tba.addInformation("scale", scaleName)
                    raise
                try:
                    rightFingeringDic = generate_right_fingering_dic(baseNote, intervals)
                except TooBigAlteration as tba:
                    tba.addInformation("hand", "right")
                    tba.addInformation("base note", baseNote)
                    tba.addInformation("scale", scaleName)
                    raise
                if not leftFingeringDic or not rightFingeringDic:
                    print("""Warning:scale "%s" starting on "%s" can't exist !!!\n\n\n""" % (
                    scaleName, baseNote.get_interval_name()), file=sys.stderr)
                    dont_exists.append((scaleName, baseNote))
                    continue
                else:
                    for side, sideFingering in [("left", leftFingeringDic), ("right", rightFingeringDic)]:
                        debug("%s fingering is %s" % (side, str(sideFingering)))
                        # print("Best %s fingering found is:" %side)
                        # for key in sideFingering:
                        #     print("%s: %d"%(key,sideFingering[key]))
                ((leftExtremalFinger, leftFingeringDic), penaltyLeft) = leftFingeringDic
                ((rightExtremalFinger, rightFingeringDic), penaltyRight) = rightFingeringDic
                if not penaltyRight.acceptable():
                    print("Warning:Right is not perfect on %s %s.\n%s" % (
                        baseNote.get_interval_name(), scaleName, penaltyRight.warning()), file=sys.stderr)
                if not penaltyLeft.acceptable():
                    print("Warning:Left is not perfect on %s %s.\n\n%s" % (
                        baseNote.get_interval_name(), scaleName, penaltyLeft.warning()), file=sys.stderr)
            for nbOctave in [1, 2,
                             # 3,
                             # 4,
                             ]:
                if doCompile:
                    leftIncreasing = generate_left_fingering(leftExtremalFinger, leftFingeringDic, baseNote, intervals,
                                                             nbOctave=nbOctave)
                    rightIncreasing = generate_right_fingering(rightExtremalFinger, rightFingeringDic, baseNote,
                                                               intervals, nbOctave=nbOctave)
                else:
                    leftIncreasing = [42]
                    rightIncreasing = [42]
                leftDecreasing = list(reversed(leftIncreasing))
                rightDecreasing = list(reversed(rightIncreasing))
                for kind, leftFingering, rightFingering, nbOctaveKind in [
                    ("increasing", leftIncreasing, rightIncreasing, 1),
                    ("decreasing", leftDecreasing, rightDecreasing, 1),
                    ("total", leftIncreasing[:-1] + leftDecreasing, rightIncreasing[:-1] + rightDecreasing, 2),
                    ("reverse", leftDecreasing[:-1] + leftIncreasing, rightDecreasing[:-1] + rightIncreasing, 2)
                    ]:
                    for hand, lilyCode in [
                        ("left", lily.lily.side(key, leftFingering, "left")),
                        ("right", lily.lily.side(key, rightFingering, "right")),
                        ("both", lily.lily.both(key, leftFingering, rightFingering))
                    ]:
                        fileName = "%s-%s-%s-%d-%s" % (scaleName, baseNameFile, hand, nbOctave, kind)
                        anki += (",<img src='%s.svg'>" % fileName)
                        anki_scale_file.write(",<img src='%s.svg'>" % fileName)
                        if nbOctave > 2:
                            continue
                        folder_fileName = "%s%s" % (folder_scale_note, fileName)
                        if not doCompile:
                            continue
                        scale_note_html += """<li><a href='%s.ly'/><img src='%s.svg'/></a></li>""" % (
                        fileName, fileName)
                        if os.path.isfile(folder_fileName + ".ly"):
                            debug("%s already exists." % (folder_fileName + ".ly"))
                            with open(folder_fileName + ".ly") as file:
                                last_code = file.readline()[:-1]
                                curnent_fingering = lilyCode.splitlines()[0]
                                if last_code != curnent_fingering:
                                    print(
                                        "Code is distinct, from %s to %s, we rewrite" % (last_code, curnent_fingering))
                                    compile = True
                                else:
                                    debug("same code. We do nothing")
                                    compile = False
                        else:
                            print("File does not exists, need to write it")
                            compile = True
                        if compile:
                            print("%s should be generated." % (folder_fileName))
                            lily.lily.compile_(lilyCode, folder_fileName)
            scale_note_html += """</ul>
        <footer>
        <a href="../../about.html"/>About</a><br/>
        <a href='../..'>Other scales</a><br/>
        <a href='..'>Other note of this scale</a>
        </footer>
        </body>
        </html>
        """
            with open("%sindex.html" % folder_scale_note, "w") as scale_note_file:
                scale_note_file.write(scale_note_html)

    scale_html += """</ul>
    <footer>
    <a href="../../about.html"/>About</a><br/>
    <a href='..'>Other scales</a>
    </footer>
    </body>
    </html>
    """
    with open("%sindex.html" % folder_scale, "w") as scale_file:
        scale_file.write(scale_html)

root_html += """
</ul>
<footer><a href="about.html"/>About</a></footer>
</body>
</html>
"""
with open(imageFolder + "/index.html", "w") as html_file:
    html_file.write(root_html)
with open(imageFolder + "piano/scales/about.html", "w") as html_file:
    html_file.write("""
<html><head><title>About fingerings of every scales</title></head><body>
Author: <a href="mailto:arthur@milchior.fr"/>Arthur Milchior</a>. Don't hesitate to contact me with idea about improving this set of fingerings. Or edit it yourself in <a href='https://github.com/Arthur-Milchior/generate-musical-image'/>git-hub</a>.

<p>
    The list of scales is mostly taken from the <a href='https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes'/>wikipedia's list of scale</a> and from the pages linked by it. Only scales which can be played on a keyboard (12 fingers by octave) have been considered. </p>

    <p>When multiple fingerings are possible, the "best" one is generated as follows:<ol>
    <li>
    No thumb ever play a black key.
    </li>
    <li>
    As far as possible, after a thumb over, the next note played is the one following in the diatonic scale.  </li>
    <li>The number of thumb over is minimal, with respect to previous condition </li>
    <li>
    The lowest finger on left hand (highest on right hand) is as high as possible (i.e. 5 if possible, otherwise, 4, etc..).
    </li>
    <li>
    The highest finger on left hand (lowest on right hand) is as low as possible. (i.e. thumb if possible)
    </li>
    <li>
    As far as possible, a thumb passing goes to a black key and not a white one.
    </li>
    <li>
    As far as possible, a thumb passing goes to a key whose chromatic distance is one.
    </li>
<ol>

</body></html>
    """)
with open("""piano/anki.csv""", "w") as anki_file:
    anki_file.write(anki)
with open("""piano/cant_exists.txt""", "w") as cant:
    cant.write("%s, %s" % (scaleName, baseNote.get_interval_name()))
print("piano ended")
