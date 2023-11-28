import os
import unittest
from typing import List

from lily.Interface import Lilyable
from lily.svg import clean_svg
from piano.pianonote import PianoNote
from solfege.note.set_of_notes import TestSetOfNotes
from util import _indent

lilyHeader = """"""
lowLimit = {"left": -14, "right": -3}
highLimit = {"left": 3, "right": 14}
lilyProgram = "lilypond"


def _for_list_of_notes(fingering: List[Lilyable]):
    """Generate the lilypond code to put in a staff, according to the fingering given in argument.
    
    chooseOctave is the function which, given its argument, decide which ottava is applied (if any)
    """
    return " ".join(note.lily() for note in fingering)


def _staff(key: str, fingering: List[Lilyable], for_right_hand: bool):
    """A lilypond staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    Bass for left hand and treble for right
 
    Add a comment with the complete fingering, to know whether recompilation is required. Or whether a change is due only to some meta information.
    """
    return f"""\\new Staff{{
  \\clef {"treble" if for_right_hand else "bass"}
  \\key {key} \\major
{_indent(_for_list_of_notes(fingering))}
}}"""


def comment(fingering: List[Lilyable], for_right_hand):
    return f"""{"right" if for_right_hand else "left"} hand fingering:{[note.lily_comment() for note in fingering]}"""


# octaveToLength={1:80, 2:135,4:240}
_lilyHeader = """\\version "2.20.0"
\\header{
  tagline=""
}"""


def lilypond_code_for_one_hand(key: str, notes_or_chords: List[Lilyable], for_right_hand: bool,
                               midi: bool):
    """A lilypond score, with a single staff.  

    The key is the given one.

    The notes are decorated with the fingering given in argument.

    The bass/treble key depends on the hand
    """
    midi_str = """
  \\midi{}""" if midi else ""
    return f"""{_lilyHeader}
\\score{{
  \\layout{{}}{midi_str}
{_indent(_staff(key, notes_or_chords, for_right_hand=for_right_hand))}
}}"""


def lilypond_code_for_two_hands(key: str, left_fingering: List[Lilyable], right_fingering: List[Lilyable], midi: bool):
    """A lilypond score for piano.

    The notes are decorated with the fingering given in arguments.
    """
    midi_str = """
  \\midi{}""" if midi else ""
    return f"""{_lilyHeader}
\\score{{
  \\layout{{}}{midi_str}
  \\new PianoStaff<<
{_indent(_staff(key, right_fingering, for_right_hand=True), 4)}
{_indent(_staff(key, left_fingering, for_right_hand=False), 4)}
  >>
}}"""


def chord(notes):
    return f"""\\version "2.20.0"
\\header{{
  tagline=""
}}
\\score{{
  \\new Staff{{
    \\clef treble <
{_indent("".join(note.lily() for note in notes), 6)}
    >
  }}
}}"""

def command(file_prefix: str, extension: str="svg"):
    if extension == "svg":
        return f"eog {file_prefix}.svg"
    else:
        assert extension == "pdf"
        return f"evince {file_prefix}.pdf"



def compile_(code, file_prefix, wav: bool, extension="svg", execute_lily: bool = True) -> str:
    """Write `code` in `filename`. If `execute_lily`, compile it in a file with the given extension

    return the command to see the generated file.
    `execute_lily` should be False only for tests, to save time.
    wav: whether to convert midi to wav. Assumes the lilypond file will generate midi."""
    if os.path.isfile(file_prefix + ".ly"):
        if os.path.exists(f"{file_prefix}.svg"):
            with open(file_prefix + ".ly", "r") as file:
                old_code = file.read()
                if old_code == code:
                    print("""%s.ly's old code is equal to current one""" % file_prefix)
                    execute_lily = False
    with open(file_prefix + ".ly", "w") as file:
        file.write(code)
    if not execute_lily:
        return command(file_prefix, extension)
    preview_path = f"{file_prefix}.preview.{extension}"
    if extension == "svg":
        os.system(f"""{lilyProgram} -dpreview -dbackend=svg -o "{file_prefix}"  "{file_prefix}.ly" """)
        clean_svg(preview_path, preview_path, "white")
    else:
        assert extension == "pdf"
        os.system( f"""lilypond  -o "{file_prefix}" "{file_prefix}.ly" """)
    os.system(f"""mv -f "{preview_path}" "{file_prefix}.{extension}" """)
    if wav:
        os.system(f"""timidity "{file_prefix}.midi" --output-mode=w -o "{file_prefix}.wav" """)
    return command(file_prefix, extension)
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

    both_hand_lily = """\\version "2.20.0"
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

    chords_lily = """\\version "2.20.0"
\\header{
  tagline=""
}
\\score{
  \\layout{}
  \\midi{}
  \\new Staff{
    \\clef bass
    \\key ees \\major
    \\clef treble <
      c'
      ees'
      g'
    > \\clef treble <
      f'
      aes'
      c''
    >
  }
}"""

    def test_indent(self):
        self.assertEquals(_indent("""foo
  bar"""), """  foo
    bar""")

    def test_for_list_of_notes(self):
        self.assertEquals(_for_list_of_notes([PianoNote(chromatic=0, diatonic=0, finger=1)], ),
                          "c'-1")
        self.assertEquals(_for_list_of_notes(self.c_pentatonic_minor_5th_right, ),
                          "c'-1 ees'-2 g'-3 c''-5")

    def test_staff(self):
        self.assertEquals(
            _staff(key="g", fingering=self.c_pentatonic_minor_5th_right, for_right_hand=True, ),
            """\\new Staff{
  \\clef treble
  \\key g \\major
  c'-1 ees'-2 g'-3 c''-5
}"""
        )

    def test_lilypond_for_right(self):
        generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_right,
                                               for_right_hand=True
                                               , midi=False)
        self.assertEquals(
            generated,
            """\\version "2.20.0"
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
        generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_left,
                                               for_right_hand=False
                                               , midi=False)
        self.assertEquals(
            generated,
            """\\version "2.20.0"
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
                                                right_fingering=self.c_pentatonic_minor_5th_right
                                                , midi=False)
        self.assertEquals(
            generated, """\\version "2.20.0"
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
        generated = lilypond_code_for_one_hand(key="g", notes_or_chords=self.c_pentatonic_minor_5th_left,
                                               for_right_hand=False
                                               , midi=True)
        self.assertEquals(
            generated,
            self.both_hand_lily
        )

    def test_lilypond_chords_generate(self):
        chords = [TestSetOfNotes.C_minor, TestSetOfNotes.F_minor]
        generated = lilypond_code_for_one_hand(key="ees", notes_or_chords=chords,
                                               for_right_hand=False, midi=True)
        self.assertEquals(
            generated,
            self.chords_lily
        )

    def test_lilypond_both_hands_and_midi(self):
        generated = lilypond_code_for_two_hands(key="g", left_fingering=self.c_pentatonic_minor_5th_left,
                                                right_fingering=self.c_pentatonic_minor_5th_right, midi=True)
        self.assertEquals(
            generated, """\\version "2.20.0"
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
        generated = chord(self.c_pentatonic_minor_5th_right, )
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
        prefix_path = "test_arpeggio"
        lily_path = f"{prefix_path}.ly"
        if os.path.isfile(lily_path):
            os.remove(lily_path)  # in case it remains from failed test
        cmd = compile_(self.both_hand_lily, prefix_path, wav=True)
        self.assertEquals(f"eog {prefix_path}.svg", cmd)
        self.assertTrue(os.path.isfile(lily_path))
        with open(lily_path, "r") as file:
            file_content = file.read()
        self.assertEquals(file_content, self.both_hand_lily)
        os.system(cmd)
        os.system(f"vlc {prefix_path}.wav")

    def test_chord_compile(self):
        prefix_path = "test_chords"
        lily_path = f"{prefix_path}.ly"
        if os.path.isfile(lily_path):
            os.remove(lily_path)  # in case it remains from failed test
        cmd = compile_(self.chords_lily, prefix_path, wav=True)
        self.assertEquals(f"eog {prefix_path}.svg", cmd)
        self.assertTrue(os.path.isfile(lily_path))
        with open(lily_path, "r") as file:
            file_content = file.read()
        self.assertEquals(file_content, self.chords_lily)
        os.system(cmd)
        os.system(f"vlc {prefix_path}.wav")
