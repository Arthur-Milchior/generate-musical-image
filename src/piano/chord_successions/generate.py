import unittest
from dataclasses import dataclass
from typing import List

from lily.Lilyable.piano_lilyable import lilypond_code_for_two_hands, lilypond_code_for_one_hand
from solfege.key import sets_of_enharmonic_keys
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes
from solfege.scale.scale import Scale
from solfege.scale.scale_pattern import major_scale


@dataclass(frozen=True)
class ChordPattern:
    name: str
    intervals: List[int]


triad = ChordPattern("triad", [2, 2])
seventh = ChordPattern("seventh", [2, 2, 2])

chord_patterns = [triad, seventh]

Succession = List[SetOfNotes]


def chord_from_scale_pattern_and_position_key(scale: Scale, chord_pattern: ChordPattern, position: int) -> SetOfNotes:
    chord = []
    for interval in [0] + chord_pattern.intervals:
        position = position + interval
        chord.append(scale.notes[position])
    return SetOfNotes(chord, fundamental=chord[0])


@dataclass(frozen=True)
class NamedSuccessionForScaleKey:
    successions: Succession
    name: str


def chord_succession_from_scale_pattern_and_position_key(scale: Scale, chord_pattern: ChordPattern,
                                                         nb_of_chords: int) -> Succession:
    return [chord_from_scale_pattern_and_position_key(scale, chord_pattern, position) for position in
            range(nb_of_chords)]


@dataclass(frozen=True)
class CardContent:
    name_prefix: str
    filepath: str
    lily_code: str

    def to_html(self) -> str:
        return f"""<img src="{self.name_prefix}.svg">"""


def succession_for_hands_key_pattern_direction(
        folder_path: str, key: Note, right_succession: Succession, chord_pattern: ChordPattern, for_left_hand: bool,
        for_right_hand: bool, direction: str, midi: bool
) -> CardContent:
    if for_left_hand:
        if for_right_hand:
            hand_name = "both"
        else:
            hand_name = "left"
    else:
        assert for_right_hand
        hand_name = "right"
    filename_prefix = f"{key.get_ascii_name()}_{hand_name}_{chord_pattern.name}_{direction}"
    filepath = f"{folder_path}/{filename_prefix}"
    left_succession = [succession.add_octaves(-1) for succession in right_succession]
    if for_left_hand and for_right_hand:
        code = lilypond_code_for_two_hands(
            key=key.lily_in_scale(), left_fingering=left_succession, right_fingering=right_succession, midi=midi
        )
    else:
        code = lilypond_code_for_one_hand(key.lily_in_scale(), left_succession if for_left_hand else right_succession,
                                          for_right_hand=for_right_hand, midi=midi)
    return CardContent(filename_prefix, filepath, code)


def succession_for_key_pattern_direction(
        folder_path: str, key: Note, right_succession: Succession, chord_pattern: ChordPattern, direction: str,
        midi: bool
) -> List[CardContent]:
    cards: List[CardContent] = []
    for (for_left_hand, for_right_hand) in [
        (True, False),
        (False, True),
        (True, True),
    ]:
        cards.append(
            succession_for_hands_key_pattern_direction(folder_path, key, right_succession, chord_pattern, for_left_hand,
                                                       for_right_hand, direction, midi))
    return cards


@dataclass(frozen=True)
class ChordSuccessionNote:
    successions: List[CardContent]
    key: Note
    chord_pattern: ChordPattern

    def to_anki(self) -> str:
        return ",".join([
                            self.chord_pattern.name,
                            self.key.get_symbol_name(),
                            "", "single octave", "",
                        ] + [
                            succession.to_html() for succession in self.successions])


def succession_for_key_pattern(
        folder_path: str, key: Note, right_succession_increasing: Succession, chord_pattern: ChordPattern,
        midi: bool
) -> ChordSuccessionNote:
    right_succession_decreasing = list(reversed(right_succession_increasing))
    right_succession_total = right_succession_increasing[:-1] + right_succession_decreasing
    right_succession_inverse = right_succession_decreasing[:-1] + right_succession_increasing
    cards: List[CardContent] = []
    for (name, right_succession) in [
        ("increasing", right_succession_increasing),
        ("decreasing", right_succession_decreasing),
        ("total", right_succession_total),
        ("inverse", right_succession_inverse),
    ]:
        cards += succession_for_key_pattern_direction(folder_path, key, right_succession, chord_pattern, name, midi)
    return ChordSuccessionNote(cards, key, chord_pattern)


def successions_for_pattern(
        folder_path: str, chord_pattern: ChordPattern, midi: bool
) -> List[ChordSuccessionNote]:
    notes: List[ChordSuccessionNote] = []
    for set_of_enharmonic_keys in sets_of_enharmonic_keys:
        key = set_of_enharmonic_keys[0].note
        scale = major_scale.generate(key, 2)
        right_succession_increasing = chord_succession_from_scale_pattern_and_position_key(
            scale, chord_pattern, nb_of_chords=major_scale.number_of_intervals() + 1
        )

        successions_all_hands_direction = succession_for_key_pattern(folder_path, key, right_succession_increasing,
                                                                     chord_pattern,
                                                                     midi)
        notes.append(successions_all_hands_direction)
    return notes


def successions(folder_path: str, midi: bool) -> List[ChordSuccessionNote]:
    notes: List[ChordSuccessionNote] = []
    for chord_pattern in [triad, seventh]:
        notes += successions_for_pattern(folder_path, chord_pattern, midi)
    return notes


class TestChordSuccession(unittest.TestCase):
    maxDiff = None

    scale = Scale([
        Note("C"),
        Note("D"),
        Note("E"),
        Note("F"),
        Note("G"),
        Note("A"),
        Note("B"),
        Note("C5"),
        Note("D5"),
        Note("E5"),
        Note("F5"),
        Note("G5"),
        Note("A5"),
        Note("B5"),
        Note("C6"),
    ], pattern=major_scale)

    triad_right_succession = [
        SetOfNotes(
            [
                Note("C"),
                Note("E"),
                Note("G"),
            ],
            Note("C"),
        ),
        SetOfNotes(
            [
                Note("D"),
                Note("F"),
                Note("A"),
            ],
            Note("D"),
        ),
        SetOfNotes(
            [
                Note("E"),
                Note("G"),
                Note("B"),
            ],
            Note("E"),
        ),
        SetOfNotes(
            [
                Note("F"),
                Note("A"),
                Note("C5"),
            ],
            Note("F"),
        ),
        SetOfNotes(
            [
                Note("G"),
                Note("B"),
                Note("D5"),
            ],
            Note("G"),
        ),
        SetOfNotes(
            [
                Note("A"),
                Note("C5"),
                Note("E5"),
            ],
            Note("A"),
        ),
        SetOfNotes(
            [
                Note("B"),
                Note("D5"),
                Note("F5"),
            ],
            Note("B"),
        ),
        SetOfNotes(
            [
                Note("C5"),
                Note("E5"),
                Note("G5"),
            ],
            Note("C5"),
        ),
    ]

    lily_right_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\set Staff.printKeyCancellation = ##f
      \\clef treble
      \\key c' \\major
      <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
    }
  >>
}"""

    lily_left_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new Staff{
      \\override Staff.TimeSignature.stencil = ##f
      \\omit Staff.BarLine
      \\omit PianoStaff.SpanBar
      \\set Staff.printKeyCancellation = ##f
      \\clef bass
      \\key c' \\major
      <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
    }
  >>
}"""

    lily_both_c_triad = """\
\\version "2.20.0"
\\score{
  <<
    \\new PianoStaff<<
      \\new Staff{
        \\override Staff.TimeSignature.stencil = ##f
        \\omit Staff.BarLine
        \\omit PianoStaff.SpanBar
        \\set Staff.printKeyCancellation = ##f
        \\clef treble
        \\key c' \\major
        <c' e' g'> <d' f' a'> <e' g' b'> <f' a' c''> <g' b' d''> <a' c'' e''> <b' d'' f''> <c'' e'' g''>
      }
      \\new Staff{
        \\set Staff.printKeyCancellation = ##f
        \\clef bass
        \\key c' \\major
        <c e g> <d f a> <e g b> <f a c'> <g b d'> <a c' e'> <b d' f'> <c' e' g'>
      }
    >>
  >>
}"""

    def test_chord_from_scale_pattern_and_position_key(self):
        son = chord_from_scale_pattern_and_position_key(
            self.scale,
            chord_pattern=triad,
            position=3,
        )
        self.assertEquals(son, SetOfNotes(
            [
                Note("F"),
                Note("A"),
                Note("C5"),
            ],
            Note("F"),
        ))

    def test_chord_succession_from_scale_pattern_and_position_key(self):
        suc = chord_succession_from_scale_pattern_and_position_key(
            self.scale,
            chord_pattern=triad,
            nb_of_chords=8,
        )
        self.assertEquals(suc,
                          self.triad_right_succession
                          )

    def test_succession_for_hands_key_pattern_direction_right(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=False, for_right_hand=True,
            direction="increasing", midi=False
        )
        self.assertEquals(suc,
                          CardContent("C______right_triad_increasing", "folder/C______right_triad_increasing",
                                      self.lily_right_c_triad)
                          )

    def test_succession_for_hands_key_pattern_direction_both(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=True,
            direction="increasing", midi=False
        )
        self.assertEquals(suc.lily_code, self.lily_both_c_triad)
        self.assertEquals(suc,
                          CardContent("C______both_triad_increasing", "folder/C______both_triad_increasing",
                                      self.lily_both_c_triad)
                          )

    def test_succession_for_hands_key_pattern_direction_left(self):
        suc = succession_for_hands_key_pattern_direction(
            "folder", Note("C"), self.triad_right_succession, triad, for_left_hand=True, for_right_hand=False,
            direction="increasing", midi=False
        )
        cc = CardContent("C______left_triad_increasing", "folder/C______left_triad_increasing",
                                      self.lily_left_c_triad)
        print(suc)
        print(cc)
        self.assertEquals(suc, cc)
