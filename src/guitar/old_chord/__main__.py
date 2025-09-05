"""Consider each way to place fingers on at least four of the six strings.
If its a chord, satisfying some condition, the image is generated, and an anki note is also generated. 
"""

# anki: open/tranposable, starting note(for open),position of tonic (for transposable), 3, 5, 7 (,image,1, 3, 5, 7)*n

from utils.util import *
from guitar.old_chord.util import *
from guitar.old_chord.set_of_chords import allChords
import guitar.util
import lily.lily

leafFolder = "chord/"
imageFolder = guitar.util.imageFolder + leafFolder
ankiFolder = guitar.util.ankiFolder + leafFolder

anki = {"open": set(), "transposable": set()}
index = dict()
for kind in anki:
    #     index[kind] = """<html><head><title>All %s chord on a standard guitar</title></head>
    # <body>
    # Here is the list of the chords, satisfying the followins properties:
    # <ul><li>
    # At least four strings are played.
    # </li><li>
    # Either a string is opened. Otherwise a finger on fret 1 is played.
    # </li><li>
    # At most four fingers used. First string is potentially barred. (Either entirely, or not at all. Todo: allow partial bar)
    # </li><li>
    # No more than four frets of difference between lowest and highest fret played.
    # </li><li>
    # The chord is not contained in another chord with the same lowest note
    # </li><li>
    # The chord is not reversed (todo: do it)
    # </li>
    # </ul>
    # The set of chords:
    # <ul>"""%kind
    pass

greatestSet = allChords.getGreatests()
longest = len(greatestSet)
for set_ in allChords:
    chord = set_.getOneElement()
    kind = chord.kind()
    pos_of_lowest_note = chord.get_most_grave_note()
    pattern_name = chord.get_pattern_name()
    if pattern_name is None or kind is None:
        raise
    subfolder = "%s/%s/" % (kind, pattern_name)
    if chord.is_open():
        subfolder += "%s/" % pos_of_lowest_note.file_name("treble")

    localImage = "%s%s" % (imageFolder, subfolder)
    localAnki = "%s%s" % (ankiFolder, subfolder)
    ensure_folder(localAnki)
    ensure_folder(localImage)
    ankiLine = "\n%s,%s,%s,%s,%s," % (kind, pos_of_lowest_note.file_name("treble"), set_.third, set_.fifth, set_.quality)
    for chord in set_:
        for (color_name, color) in [("color", True), ("black", False)]:
            fileName = chord.file_name()
            fileName_color = f"{fileName}_{color_name}.svg"
            ankiLine += f"""",<img src="{fileName_color}"/>"""
            with open(localImage + fileName_color, "w") as f:
                chord.draw(f, color=color)
            chordFile = f"{localImage}{fileName}_chord_{color_name}"
            code = chord.lily()
            lily.lily.compile_(code, chordFile, wav=False)

        ankiLine += f""",{chord.content_of_anki_csv()},<img src="{chordFile}"/>"""
        # index[kind] += """<li><a href='%s'>%s</li>"""%(fileName, patternName)
    ankiLine += ",,,,,,," * (len(set_) - longest)
    anki[kind].add(ankiLine)

ensure_folder(ankiFolder)
ensure_folder(imageFolder + "transposable/")
ensure_folder(imageFolder + "open/")
for kind in anki:
    # index[kind] += "</ul></body></hmtl>"
    save_file(ankiFolder + "anki_" + kind + ".csv", "\n".join(anki[kind]))
    # with open(imageFolder+kind+"/index.html","w") as f:
    #     f.write(index[kind])

print("There is up to %d version of the same chord, i.e. chord %s" % (longest, str(greatestSet)))
