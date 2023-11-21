import os
import unittest
from typing import List

from piano.pianonote import PianoNote
from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note

lilyHeader = """"""
lowLimit = {"left": -14, "right": -3}
highLimit = {"left": 3, "right": 14}
lilyProgram = "lilypond"


def _indent(str: str, nb_space: int = 2):
    return "\n".join(f"""{" " * nb_space}{line}""" for line in str.split("\n"))


def _for_list_of_notes(fingering: List[PianoNote], use_color=True):
    """Generate the lilypond code to put in a staff, according to the fingering given in argument.
    
    chooseOctave is the function which, given its argument, decide which ottava is applied (if any)
    """
    return " ".join(note.lily(use_color=use_color) for note in fingering)


def _staff(key: str, fingering: List[PianoNote], for_right_hand: bool, use_color=True):
    """A lilypond staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    Bass for left hand and treble for right
 
    Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
    """
    return f"""\\new Staff{{
  \\clef {"treble" if for_right_hand else "bass"}
  \\key {key} \\major
{_indent(_for_list_of_notes(fingering, use_color=use_color))}
}}"""


def comment(fingering: List[PianoNote], for_right_hand):
    return f"""{"right" if for_right_hand else "left"} hand fingering:{[note.finger for note in fingering]}"""


# octaveToLength={1:80, 2:135,4:240}
_lilyHeader = """\\version "2.20.0"
\\header{
  tagline=""
}"""


def lilypond_code_for_one_hand(key: str, fingering: List[PianoNote], for_right_hand: bool, use_color: bool,
                               midi: bool):
    """A lilypond score, with a single staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    The bass/treble key depends on the hand
    """
    midi_str = """
  \\midi{}""" if midi else ""
    return f"""%%{comment(fingering, for_right_hand=for_right_hand)}
{_lilyHeader}
\\score{{
  \\layout{{}}{midi_str}
{_indent(_staff(key, fingering, for_right_hand=for_right_hand, use_color=use_color))}
}}"""


def lilypond_code_for_two_hands(key: str, left_fingering: List[PianoNote], right_fingering: List[PianoNote],  midi: bool,
                                use_color=True,):
    """A lilypond score for piano.

    The notes are decorated with the fingering given in arguments.
    """
    midi_str = """
  \\midi{}""" if midi else ""
    return f"""%%{comment(left_fingering, False)}, {comment(right_fingering, True)}
{_lilyHeader}
\\score{{
  \\layout{{}}{midi_str}
  \\new PianoStaff<<
{_indent(_staff(key, right_fingering, for_right_hand=True, use_color=use_color), 4)}
{_indent(_staff(key, left_fingering, for_right_hand=False, use_color=use_color), 4)}
  >>
}}"""


def chord(notes, use_color=True):
    return f"""\\version "2.20.0"
\\header{{
  tagline=""
}}
\\score{{
  \\new Staff{{
    \\clef treble <
{_indent("".join(note.lily(use_color=use_color) for note in notes), 6)}
    >
  }}
}}"""


def compile_(code, fileName, wav: bool, extension="svg", execute_lily: bool = True):
    """Write `code` in `filename`. If `execute_lily`, compile it in a file with the given extension

    `execute_lily` should be False only for tests, to save time.
    wav: whether to convert midi to wav. Assumes the lilypond file will generate midi."""
    if os.path.isfile(fileName + ".ly"):
        with open(fileName + ".ly", "r") as file:
            old_code = file.read()
            if old_code == code:
                print("""%s.ly's old code is equal to current one""" % fileName)
                return
    with open(fileName + ".ly", "w") as file:
        file.write(code)
    if not execute_lily:
        return
    if extension == "svg":
        command = f"""{lilyProgram} -dpreview -dbackend=svg -o "{fileName}"  "{fileName}.ly" """
    else:
        assert extension == "pdf"
        command = f"""lilypond  -o "{fileName}" "{fileName}.ly" """
    os.system(command)
    os.system(f"""mv -f "{fileName}.preview.{extension}" "{fileName}.{extension}" """)
    if wav:
        os.system(f"""timidity "{fileName}.midi" --output-mode=w -o "{fileName}.wav" """)
    # os.system("""inkscape --verb=FitCanvasToDrawing --verb=FileSave --verb=FileClose "%s.svg"&"""%(folder_fileName))
    # os.system("""convert -background "#FFFFFF" -flatten "%s.svg" "%s.png" """%(folder_fileName,folder_fileName))


class TestLily(unittest.TestCase):
    c_pentatonic_minor_5th_right = [
        PianoNote(chromatic=0, diatonic=0, finger=1),
        PianoNote(chromatic=3, diatonic=2, finger=2),
        PianoNote(chromatic=7, diatonic=4, finger=3),
        PianoNote(chromatic=12, diatonic=7, finger=5),
    ]

    c_pentatonic_minor_5th_left = [
        PianoNote(chromatic=-12, diatonic=-7, finger=5),
        PianoNote(chromatic=-9, diatonic=-5, finger=3),
        PianoNote(chromatic=-5, diatonic=-3, finger=2),
        PianoNote(chromatic=0, diatonic=0, finger=1),
    ]

    both_hand_lily = """%%left hand fingering:[5, 3, 2, 1], right hand fingering:[1, 2, 3, 5]
\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\midi{}
  \\new PianoStaff<<
    \\new Staff{
      \\clef treble
      \\key g \\major
      c'-1 ees'-2 g'-3 c''-5
    }
    \\new Staff{
      \\clef bass
      \\key g \\major
      c-5 ees-3 g-2 c'-1
    }
  >>
}"""

    def test_indent(self):
        self.assertEquals(_indent("""foo
  bar"""), """  foo
    bar""")

    def test_for_list_of_notes(self):
        self.assertEquals(_for_list_of_notes([PianoNote(chromatic=0, diatonic=0, finger=1)], use_color=False),
                          "c'-1")
        self.assertEquals(_for_list_of_notes(self.c_pentatonic_minor_5th_right, use_color=False),
                          "c'-1 ees'-2 g'-3 c''-5")

    def test_staff(self):
        self.assertEquals(
            _staff(key="g", fingering=self.c_pentatonic_minor_5th_right, for_right_hand=True, use_color=False),
            """\\new Staff{
  \\clef treble
  \\key g \\major
  c'-1 ees'-2 g'-3 c''-5
}"""
        )

    def test_lilypond_for_right(self):
        generated = lilypond_code_for_one_hand(key="g", fingering=self.c_pentatonic_minor_5th_right,
                                               for_right_hand=True,
                                               use_color=False, midi=False)
        self.assertEquals(
            generated,
            """%%right hand fingering:[1, 2, 3, 5]
    \\version "2.20.0"
    \\header{
      tagline=""
    }
    \\score{
      \\new Staff{
        \\clef treble
        \\key g \\major
        c'-1 ees'-2 g'-3 c''-5
      }
    }"""
            )

    def test_lilypond_for_left(self):
        generated = lilypond_code_for_one_hand(key="g", fingering=self.c_pentatonic_minor_5th_left,
                                               for_right_hand=False,
                                               use_color=False, midi=False)
        self.assertEquals(
            generated,
            """%%left hand fingering:[5, 3, 2, 1]
\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\new Staff{
    \\clef bass
    \\key g \\major
    c-5 ees-3 g-2 c'-1
  }
}"""
        )

    def test_lilypond_both_hands(self):
        generated = lilypond_code_for_two_hands(key="g", left_fingering=self.c_pentatonic_minor_5th_left,
                                                right_fingering=self.c_pentatonic_minor_5th_right,
                                                use_color=False, midi=False)
        self.assertEquals(
            generated, """%%left hand fingering:[5, 3, 2, 1]
\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\new Staff{
    \\clef bass
    \\key g \\major
    c-5 ees-3 g-2 c'-1
  }
}"""
        )

    def test_lilypond_for_left_and_midi(self):
        generated = lilypond_code_for_one_hand(key="g", fingering=self.c_pentatonic_minor_5th_left,
                                               for_right_hand=False,
                                               use_color=False, midi=True)
        self.assertEquals(
            generated,
            self.both_hand_lily
        )

    def test_lilypond_both_hands_and_midi(self):
        generated = lilypond_code_for_two_hands(key="g", left_fingering=self.c_pentatonic_minor_5th_left,
                                                right_fingering=self.c_pentatonic_minor_5th_right,
                                                use_color=False, midi=True)
        self.assertEquals(
            generated, """%%left hand fingering:[5, 3, 2, 1], right hand fingering:[1, 2, 3, 5]
\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\midi{}
  \\new PianoStaff<<
    \\new Staff{
      \\clef treble
      \\key g \\major
      c'-1 ees'-2 g'-3 c''-5
    }
    \\new Staff{
      \\clef bass
      \\key g \\major
      c-5 ees-3 g-2 c'-1
    }
  >>
}"""
        )

    def test_chord(self):
        generated = chord(self.c_pentatonic_minor_5th_right, use_color=False)
        self.assertEquals(generated,
                          """\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\new Staff{
    \\clef treble <
      c'-1ees'-2g'-3c''-5
    >
  }
}""")

    def test_compile(self):
        lily_path = "test.ly"
        if os.path.isfile(lily_path):
            os.remove(lily_path)  # in case it remains from failed test
        compile_(self.both_hand_lily, "test", wav=True)
        self.assertTrue(os.path.isfile(lily_path))
        with open(lily_path, "r") as file:
            file_content = file.read()
        self.assertEquals(file_content, self.both_hand_lily)
        os.system("eog test.svg")
        os.system("vlc test.wav")
