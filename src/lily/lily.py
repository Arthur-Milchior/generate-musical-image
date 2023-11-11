from solfege.interval import TooBigAlteration
import os
import math
from solfege.note import Note

lilyHeader = """"""
lowLimit = {"left": -14, "right": -3}
highLimit = {"left": 3, "right": 14}
lilyProgram = "lilypond"


def _defaultOctave(note, finger, restart=None):
    """Right now, ottava is never used, so the function always return zero"""
    return 0


def _actualFinger(fingering, side, chooseOctave=_defaultOctave):
    """Generate the lilypond code to put in a staff, according to the fingering given in argument.
    
    side state whether left hand or right hand is generated.
    
    chooseOctave is the function which, given its argument, decide which ottava is applied (if any)
    """
    text = ""
    lastOctave = None
    for (note, finger) in fingering:
        assert (isinstance(note, Note))
        octave = chooseOctave(note, finger)
        height = note.getDiatonic().getNumber()
        if octave != lastOctave:
            text += "\ottava #%d\n" % (octave)
            lastOctave = octave
        text += """%s-%d
""" % (note.lily(), finger)
    return text


def _staff(key, fingering, side):
    """A lilypond staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    The bass/treble key depends on the given side
 
    Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
    """
    return """
\\new Staff{
    \\clef %s
    \\key %s \\major
%s}
""" % ({"left": "bass", "right": "treble"}[side], key, _actualFinger(fingering, side))


def comment(fingering, side):
    return """%%%s hand fingering:%s""" % (side, [finger for (note, finger) in fingering])


# octaveToLength={1:80, 2:135,4:240}
_lilyHeader = """#(set-default-paper-size "a4" 'landscape)
\\version "2.18.2"
            \\header{
            tagline=""
            }
            """


def side(key, fingering, side):
    """A lilypond score, with a single staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    The bass/treble key depends on the given side
    """
    return ("""%s
        %s\\score{
        %s}
        """ % (  # length,
        comment(fingering, side),
        _lilyHeader,
        _staff(key, fingering, side)))


def both(key, leftFingering, rightFingering):
    """A lilypond score for piano.

    The notes are decorated with the fingering given in arguments.
    """
    return ("""%s%s
        %s\\score{
            \\new PianoStaff<<
            %s
            %s
            >>
            }""" % (  # length,
        comment(leftFingering, "left"),
        comment(rightFingering, "right"),
        _lilyHeader,
        _staff(key, rightFingering, "right"), _staff(key, leftFingering, "left")))


def chord(notes, color=True):
    text = """\\version "2.18.2"
            \\header{
            tagline=""
            }
            \\score{

            
\\new Staff{
    \\clef treble
<
"""
    for note in notes:
        try:
            text += note.lily(color=color)
        except TooBigAlteration as tba:
            tba.addInformation("notes", notes)
            raise
    text += """>}}"""
    return text


def compile_(code, fileName, extension="svg"):
    """Write the code in the file, and compile it in a file with the given extension"""
    if os.path.isfile(fileName + ".ly"):
        with open(fileName + ".ly", "r") as file:
            old_code = file.read()
            if old_code == code:
                print("""%s.ly's old code is equal to current one""" % fileName)
                return
    with open(fileName + ".ly", "w") as file:
        file.write(code)
    if extension == "svg":
        os.system("""%s -dpreview -dbackend=svg -o "%s"  "%s.ly" """ % (lilyProgram, fileName, fileName))
    elif extension == "pdf":
        os.system("""lilypond  -o "%s" "%s.ly" """ % (fileName, fileName))
    os.system("""mv -f "%s.preview.%s" "%s.%s" """ % (fileName, extension, fileName, extension))
    # os.system("""inkscape --verb=FitCanvasToDrawing --verb=FileSave --verb=FileClose "%s.svg"&"""%(folder_fileName))
    # os.system("""convert -background "#FFFFFF" -flatten "%s.svg" "%s.png" """%(folder_fileName,folder_fileName))
