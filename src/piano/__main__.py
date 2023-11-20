import os
import pathlib
import sys
from dataclasses import dataclass
from typing import List, Union

import util
from lily.lily import lilypond_code_for_two_hands, lilypond_code_for_one_hand, compile_
from piano.Fingering.fingering import Fingering
from piano.generate import generate_fingering
from piano.pianonote import PianoNote
from solfege.Scale.pattern import ScalePattern
from solfege.clef import clefs
from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.note import Note
from solfege.note.alteration import TEXT, FILE_NAME, LILY, MONOSPACE

leafFolder = "piano/scales/"
imageFolder = util.imageFolder + leafFolder
ankiFolder = util.ankiFolder + leafFolder

INCREASING = "increasing"
DECREASING = "decreasing"
TOTAL = "total"
REVERSE = "reverse"

doCompile = True

"""The root of the web page to navigate fingering of scales."""
lines_of_root_html = ["""<html><head><title>Fingerings of every scales</title></head><body>
<header><h1>Fingerings of every scales</h1></header>
<ul>"""]

content_of_anki_csv = []

scales_the_algorithm_failed_to_generate = []


@dataclass
class ScoreFixedPatternFirstNoteDirectionNumberOfOctavesLeftOrRightOrBoth:
    image_tag: str
    html_line: str


def generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both(scale_name: str,
                                                                                              folder_path: str,
                                                                                              scale_lowest_note: Note,
                                                                                              show_left: bool,
                                                                                              show_right: bool,
                                                                                              number_of_octaves: int,
                                                                                              direction: str,
                                                                                              lily_code: str,
                                                                                              execute_lily: bool,
                                                                                              ) -> ScoreFixedPatternFirstNoteDirectionNumberOfOctavesLeftOrRightOrBoth:
    """Ensure that folder_path/ contains the score for lilyCode, for scale_name, hands left/right, number_of_octaves and direction.
    Don't compile if `compile` is false. Mostly used for testing"""
    assert show_right or show_left
    file_name = f"""{scale_name}-{scale_lowest_note.get_note_name(FILE_NAME)}-{("two_hands" if show_left else "right_hand") if show_right else "left_hand"}-{number_of_octaves}-{direction}"""
    image_tag = f"<img src='{file_name}.svg'>"
    file_path = f"{folder_path}/{file_name}"
    html_line = f"<li><a href='{file_name}.ly'/>{image_tag}</a></li>"
    # In case the current file already exists with same content, we avoid rebuilding it
    if os.path.isfile(file_path + ".ly"):
        with open(file_path + ".ly") as file:
            last_code = file.readline()[:-1]  # Line containing first fingering
            current_fingering = lily_code.splitlines()[0]
            if last_code != current_fingering:
                compile_(lily_code, file_path, execute_lily=execute_lily)
    else:
        compile_(lily_code, file_path, execute_lily=execute_lily)
    return ScoreFixedPatternFirstNoteDirectionNumberOfOctavesLeftOrRightOrBoth(image_tag=image_tag, html_line=html_line)


@dataclass
class ScoreFixedPatternFirstNoteNumberOfOctaves:
    image_tags: List[str]
    html_lines: List[str]


def generate_score_fixed_pattern_first_note_direction_number_of_octaves(key: str,
                                                                        scale_lowest_note: Note,
                                                                        left_scale_fingering: List[PianoNote],
                                                                        right_scale_fingering: List[PianoNote],
                                                                        scale_name: str,
                                                                        folder_path: str,
                                                                        number_of_octaves: int,
                                                                        direction: str,
                                                                        execute_lily: bool,
                                                                        ) -> ScoreFixedPatternFirstNoteNumberOfOctaves:
    anki_fields_for_this_note_scale_direction = []
    html_lines = []
    try:
        left_code = lilypond_code_for_one_hand(key=key,
                                               fingering=left_scale_fingering,
                                               for_right_hand=False, use_color=False)
    except TooBigAlterationException as tba:
        tba["fingering"] = left_scale_fingering
        raise
    try:
        right_code = lilypond_code_for_one_hand(key=key,
                                                fingering=right_scale_fingering,
                                                for_right_hand=True, use_color=False)
    except TooBigAlterationException as tba:
        tba["fingering"] = right_scale_fingering
        raise
    both_hands_code = lilypond_code_for_two_hands(key=key,
                                                  left_fingering=left_scale_fingering,
                                                  right_fingering=right_scale_fingering, use_color=False)
    for show_left, show_right, lily_code in [
        (True, False, left_code),
        (False, True, right_code),
        (True, True, both_hands_code)
    ]:
        output = generate_score_fixed_pattern_first_note_direction_number_of_octaves_left_or_right_or_both(
            folder_path=folder_path,
            scale_name=scale_name, scale_lowest_note=scale_lowest_note,
            show_left=show_left, show_right=show_right,
            number_of_octaves=number_of_octaves, direction=direction,
            lily_code=lily_code,
            execute_lily=execute_lily,
        )
        anki_fields_for_this_note_scale_direction.append(output.image_tag)
        html_lines.append(output.html_line)
    return ScoreFixedPatternFirstNoteNumberOfOctaves(anki_fields_for_this_note_scale_direction, html_lines)


def generate_score_fixed_pattern_first_note_number_of_octaves(key: str,
                                                              right_hand_lowest_note: Note,
                                                              scale_pattern: ScalePattern,
                                                              left_fingering: Fingering,
                                                              right_fingering: Fingering,
                                                              folder_path: str,
                                                              number_of_octaves: int,
                                                              execute_lily: bool,
                                                              ) -> ScoreFixedPatternFirstNoteNumberOfOctaves:
    anki_fields_for_this_scale_pattern_lowest_note_and_number_of_octaves = []
    html_lines = []
    left_hand_scale_increasing = left_fingering.generate(first_played_note=right_hand_lowest_note.add_octave(-1),
                                                         scale_pattern=scale_pattern,
                                                         number_of_octaves=number_of_octaves)
    right_hand_scale_increasing = right_fingering.generate(first_played_note=right_hand_lowest_note,
                                                           scale_pattern=scale_pattern,
                                                           number_of_octaves=number_of_octaves)
    left_hand_scale_decreasing = list(reversed(left_hand_scale_increasing))
    right_hand_scale_decreasing = list(reversed(right_hand_scale_increasing))
    for direction, left_scale_fingering, right_scale_fingering in [
        (INCREASING, left_hand_scale_increasing, right_hand_scale_increasing),
        (DECREASING, left_hand_scale_decreasing, right_hand_scale_decreasing),
        (TOTAL, left_hand_scale_increasing[:-1] + left_hand_scale_decreasing,
         right_hand_scale_increasing[:-1] + right_hand_scale_decreasing),
        (REVERSE, left_hand_scale_decreasing[:-1] + left_hand_scale_increasing,
         right_hand_scale_decreasing[:-1] + right_hand_scale_increasing)
    ]:
        try:
            output = generate_score_fixed_pattern_first_note_direction_number_of_octaves(
                key=key,
                scale_lowest_note=right_hand_lowest_note,
                left_scale_fingering=left_scale_fingering,
                right_scale_fingering=right_scale_fingering,
                scale_name=scale_pattern.get_the_first_of_the_name().replace(" ", "_"),
                # this replace is uselessly costly, as iterated many time. But this is not a bottleneck compared to lily, so never mind
                folder_path=folder_path,
                number_of_octaves=number_of_octaves,
                direction=direction,
                execute_lily=execute_lily,
            )
        except TooBigAlterationException as tba:
            tba["scale pattern"] = scale_pattern
            tba["right hand lowest note"] = str(right_hand_lowest_note)
            raise
        anki_fields_for_this_scale_pattern_lowest_note_and_number_of_octaves += output.image_tags
        html_lines += output.html_lines
    return ScoreFixedPatternFirstNoteNumberOfOctaves(
        anki_fields_for_this_scale_pattern_lowest_note_and_number_of_octaves, html_lines)


@dataclass
class ScoreFixedPatternFirstNote:
    anki_note_as_csv: str
    html_link_for_this_starting_note: str


@dataclass
class MissingFingering:
    scale_pattern: ScalePattern
    note: Note
    for_right_hand: bool

    def __str__(self):
        return f"""Missing {"right" if self.for_right_hand else "left"} {self.note} {self.scale_pattern.get_the_first_of_the_name()}"""


def generate_score_fixed_pattern_first_note(key: str,
                                            right_hand_lowest_note: Note,
                                            scale_pattern: ScalePattern,
                                            folder_path: str,
                                            execute_lily: bool,
                                            ) -> Union[ScoreFixedPatternFirstNote, List[MissingFingering]]:
    """

    Key: indication for lily about flats and sharps
    Right_hand_lowest_note: where to start the scale.

    Bot are usually similar.
    """
    left_penalty = generate_fingering(right_hand_lowest_note, scale_pattern=scale_pattern, for_right_hand=False)
    right_penalty = generate_fingering(right_hand_lowest_note, scale_pattern=scale_pattern, for_right_hand=True)
    missing_scales = []
    if not left_penalty:
        missing_scales.append(
            MissingFingering(scale_pattern=scale_pattern, note=right_hand_lowest_note, for_right_hand=False))
    if not right_penalty:
        missing_scales.append(
            MissingFingering(scale_pattern=scale_pattern, note=right_hand_lowest_note, for_right_hand=True))
    if missing_scales:
        return missing_scales
    left_fingering = left_penalty.fingering
    right_fingering = right_penalty.fingering
    anki_fields_for_this_scale_pattern_and_lowest_note = [scale_pattern.get_the_first_of_the_name(),
                                                          right_hand_lowest_note.get_note_name(MONOSPACE)]
    html_lines = []
    if not right_penalty.acceptable():
        print(
            f"Warning:Right is not perfect on {right_hand_lowest_note.get_note_name(usage=TEXT)} {scale_pattern.get_the_first_of_the_name()}.\n{right_penalty.warning()}",
            file=sys.stderr)
    if not left_penalty.acceptable():
        print(
            f"Warning:Left is not perfect on {right_hand_lowest_note.get_note_name(usage=TEXT)} {scale_pattern.get_the_first_of_the_name()}.\n{left_penalty.warning()}",
            file=sys.stderr)
    for number_of_octaves in [1, 2]:
        output = generate_score_fixed_pattern_first_note_number_of_octaves(
            key=key,
            right_hand_lowest_note=right_hand_lowest_note,
            left_fingering=left_fingering,
            right_fingering=right_fingering,
            scale_pattern=scale_pattern,
            folder_path=folder_path,
            number_of_octaves=number_of_octaves,
            execute_lily=execute_lily,
        )
        anki_fields_for_this_scale_pattern_and_lowest_note += output.image_tags
        html_lines += output.html_lines

    with open(f"{folder_path}/index.html", "w") as scale_note_file:
        scale_note_file.write(f"""\
<html>
  <head>
    <title>
      Fingerings of {right_hand_lowest_note.get_note_name(TEXT)} {scale_pattern.get_the_first_of_the_name()}
    </title>
  </head>
  <body>
    <header>
      <h1>
        Fingerings of {right_hand_lowest_note.get_note_name(TEXT)} {scale_pattern.get_the_first_of_the_name()}
      </h1>
    </header>
    <ul>
      """ + """
      """.join(html_lines) + """\
    </ul>
    <footer>
      <a href="../../about.html"/>About</a><br/>
      <a href='..'>Same scale with other first note</a>
      <a href='../..'>Other scales</a>
    </footer>
  </body>
</html>""")
    return ScoreFixedPatternFirstNote(",".join(anki_fields_for_this_scale_pattern_and_lowest_note),
                                      f"""<li><a href='{right_hand_lowest_note.get_note_name(usage=TEXT)}'>{right_hand_lowest_note.get_note_name(usage=TEXT)}</a></li>""")


@dataclass
class ScoreFixedPattern:
    # State that scale_pattern on note is missing for
    missing_scores: List[MissingFingering]
    too_big_alterations: List[TooBigAlterationException]
    html_link_for_this_scale_pattern: str
    anki_notes_as_csv: List[str]


def generate_score_fixed_pattern(scale_pattern: ScalePattern,
                                 folder_path: str,
                                 execute_lily: bool,
                                 ) -> ScoreFixedPattern:
    anki_notes_as_csv: List[str] = []
    missing: List[MissingFingering] = []
    html_lines_for_pattern: List[str] = []
    too_big_alterations: List[TooBigAlterationException] = []
    for fundamental in clefs:
        starting_note = fundamental.note - scale_pattern.interval_for_signature
        note_folder = f"{folder_path}/{starting_note.get_note_name(FILE_NAME)}"
        pathlib.Path(note_folder).mkdir(exist_ok=True)
        try:
            output = generate_score_fixed_pattern_first_note(key=fundamental.note.get_note_name(LILY),
                                                             right_hand_lowest_note=starting_note,
                                                             scale_pattern=scale_pattern,
                                                             folder_path=note_folder, execute_lily=execute_lily)
        except TooBigAlterationException as tba:
            too_big_alterations.append(tba)
            continue
        if isinstance(output, ScoreFixedPatternFirstNote):
            anki_notes_as_csv.append(output.anki_note_as_csv)
            html_lines_for_pattern.append(output.html_link_for_this_starting_note)
        else:
            missing += output
            continue
    with open(f"{folder_path}/anki.csv", "w") as anki_scale_file:
        anki_scale_file.write("\n".join(anki_notes_as_csv))
    with open(f"{folder_path}/index.html", "w") as html_scale_file:
        html_scale_file.write(f"""\
<html>
  <head>
    <title>
      Fingerings of {scale_pattern.get_the_first_of_the_name()}
    </title>
  </head>
  <body>
    <header>
      <h1>
        Fingerings of {scale_pattern.get_the_first_of_the_name()}
      </h1>
    </header>
    <ul>
      """ + """
      """.join(html_lines_for_pattern) + """\
    </ul>
    <footer>
      <a href="../about.html"/>About</a><br/>
      <a href='..'>Other scales</a>
    </footer>
  </body>
</html>""")
        return ScoreFixedPattern(
            missing_scores=missing,
            html_link_for_this_scale_pattern=f"""<li><a href='{scale_pattern.get_the_first_of_the_name().replace(" ", "_")}'>{scale_pattern.get_the_first_of_the_name()}</a></li>""",
            anki_notes_as_csv=anki_notes_as_csv,
            too_big_alterations=too_big_alterations,
        )


about_page_content = """
<html>
  <head>
    <title>
      About fingerings of every scales
    </title>
  </head>
  <body>
Author: <a href="mailto:arthur@milchior.fr"/>Arthur Milchior</a>. Don't hesitate to contact me with idea about improving this set of fingerings. Or edit it yourself in <a href='https://github.com/Arthur-Milchior/generate-musical-image'/>git-hub</a>.

<p>
    The list of scales is mostly taken from the <a href='https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes'/>wikipedia's list of scale</a> and from the pages linked by it. Only scales which can be played on a keyboard (12 fingers by octave) have been considered. </p>

    <p>When multiple fingerings are possible, the "best" one is generated as follows:
    <ol>
      <li>
        No thumb ever play a black key.
      </li>
      <li>
        As far as possible, after a thumb over, the next note played is the one following in the diatonic scale.  </li>
      <li>
        The number of thumb over is minimal, with respect to previous condition.
      </li>
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
    </ol>
  </body>
</html>
        """


@dataclass
class GenerateScoreOutput:
    missing_scores: List[MissingFingering]
    too_big_alterations: List[TooBigAlterationException]


def generate_scores(folder_path: str, execute_lily: bool) -> GenerateScoreOutput:
    missing_fingerings: List[MissingFingering] = []
    too_big_alterations = []
    html_main_index_lines = []
    anki_every_notes_as_csv: List[str] = []
    for scale_pattern in ScalePattern.class_to_patterns[ScalePattern]:
        scale_pattern_folder_path = f"""{folder_path}/{scale_pattern.get_the_first_of_the_name().replace(" ", "_")}"""
        util.ensure_folder(scale_pattern_folder_path)
        output = generate_score_fixed_pattern(
            scale_pattern=scale_pattern,
            folder_path=scale_pattern_folder_path,
            execute_lily=execute_lily,
        )
        missing_fingerings += output.missing_scores
        html_main_index_lines.append(output.html_link_for_this_scale_pattern)
        anki_every_notes_as_csv += output.anki_notes_as_csv
        too_big_alterations += output.too_big_alterations
    with open(f"{folder_path}/index.html", "w") as html_file:
        html_file.write(f"""
<html>
  <head>
    <title>
      Piano fingerings
    </title>
  </head>
  <body>
    <header>
      <h1>
        Piano fingerings
      </h1>
    </header>
    <ul>
      {{"\n".join(lines_of_root_html)}}
    </ul>
    <footer><a href="about.html"/>About</a></footer>
  </body>
</html>""")
    with open(f"{folder_path}/about.html", "w") as html_file:
        html_file.write(about_page_content)
    with open(f"""{folder_path}/anki.csv""", "w") as anki_file:
        anki_file.write("\n".join(anki_every_notes_as_csv))
    with open(f"""{folder_path}/scales_the_algo_failed_to_compute.txt""", "w") as cant:
        cant.write("\n".join(str(missing_fingering) for missing_fingering in missing_fingerings))
    with open(f"""{folder_path}/too_big_alterations.txt""", "w") as tba_file:
        tba_file.write("\n".join(repr(tba) for tba in too_big_alterations))
    return GenerateScoreOutput(missing_scores=missing_fingerings, too_big_alterations=too_big_alterations)


if __name__ == '__main__':
    folder_path = "piano"
    util.ensure_folder(folder_path)
    generate_scores(folder_path=folder_path, execute_lily=True)
