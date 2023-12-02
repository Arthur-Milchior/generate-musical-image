# It should generate:
# 63 scales
# 12 note
# 2 octaves
# 4 kinds
# 3 hands
# =18144 images
# Taking 4 seconds each, it takes 20 hours
import os
import unittest
from typing import Optional, List, Tuple, Union, Callable

from utils import util
from lily.lily import compile_, lilypond_code_for_one_hand
from piano.scales.fingering import Fingering, TestFingering
from piano.scales.penalty import Penalty
from solfege.chord.chord_pattern import minor_seven, augmented_major_seventh_chord
from solfege.scale.scale_pattern import ScalePattern, minor_melodic, blues, pentatonic_major
from solfege.note import Note
from utils.constants import test_folder

lilyProgram = "lilypond "


def generate_fingering(fundamental: Note, scale_pattern: ScalePattern, for_right_hand: bool) -> Optional[Penalty]:
    """
    Returns the best penalty extending `fingering` to add `base_note`, and then one note per interval starting at
    `base_note`.

    For the left hand, the note added are thus:
    * base_note
    * base_note + intervals[0]
    * base_note + intervals[0] + intervals[1]
     that is, the generation starts from the side of the pinky finger, from the lowest note, up to the thumb/higher
     note. On the right hand it is the reverse.

    return False if no fingering can be found
    Otherwise, return:
       --the starting finger (lowest for left hand, highest for right hand),
       --the fingering for the non-starting note
       , and
       --the penalty
    """

    scale = scale_pattern.generate(fundamental, add_an_extra_note=True, number_of_octaves=(-1 if for_right_hand else 1))
    notes = scale.notes
    pink_side_tonic = notes[0]
    other_notes = notes[1:]

    def aux(last_added_note: Note, remaining_notes: List[Note], last_added_finger: int, fingering: Fingering,
            penalty: Penalty, best_known_penalty: Optional[Penalty]) -> Optional[Penalty]:
        """
        Return the best extension of `fingering`, with `current_note` associated to `current_finger` if it exists and is less than best_known_penalty.
        Penalty -- the penalty for currently added fingers, not considering penalties associated to extremities.
        The extension should be valid for the note of [remaining_notes].
        The first of remaining_notes is the one closer to last_added_note.

         Return the best penalty if it exists.
        """
        penalty = penalty._copy(fingering=fingering)
        if last_added_note.is_black_key_on_piano() and last_added_finger == 1:
            penalty = penalty.add_thumb_on_black()
        if not remaining_notes:
            # it's okay to edit in place as `penalty` is a local variable that has no other owner
            return best_known_penalty if penalty.best_known_is_at_least_as_good(best_known_penalty) else penalty

        # on the right hand, we go from high to low. So we take the last interval and reverse it to decrease the
        # current note.
        # On the left hand, we go from low to high, so we take the first interval and use it to increase the
        # current note.
        next_note = remaining_notes[0]
        next_remaining_notes = remaining_notes[1:]

        # List of possible next finger, and potentially the way the Penalty would change using it
        next_possible_fingers: List[Union[int, Tuple[int, Callable[[Penalty], Penalty]]]]
        if last_added_finger == 1:
            if not fundamental.equals_modulo_octave(last_added_note):
                penalty = penalty.add_thumb_over()
            if not last_added_note.adjacent(next_note):
                penalty = penalty.add_thumb_non_adjacent()
            if not next_note.is_black_key_on_piano():
                penalty = penalty.add_white_after_thumb()
            next_possible_fingers = [3, 4, 2]
        elif last_added_finger == 2:
            next_possible_fingers = [1]
        elif last_added_note.adjacent(next_note):
            next_possible_fingers = [last_added_finger - 1]
        elif last_added_finger == 4:
            # non adjacent next note
            next_possible_fingers = [2, (3, (lambda penalty: penalty.add_3_and_four_non_adjacent()))]
        else:
            next_possible_fingers = [last_added_finger - 1, last_added_finger - 2]

        if penalty.best_known_is_at_least_as_good(best_known_penalty):
            return best_known_penalty

        for next_possible_finger in next_possible_fingers:
            if isinstance(next_possible_finger, tuple):
                next_possible_finger, penalty_update = next_possible_finger
            else:
                assert isinstance(next_possible_finger, int)
                penalty_update = lambda penalty: penalty

            next_fingering = fingering.add(next_note, next_possible_finger)
            if next_fingering is False:
                # Another finger is associated to this note (up to octave, and not including the starting finger)
                continue
            if next_fingering is True:
                # This association is already in the scales.
                # It should only occur in the second time we consider the second note of the scale
                # when this note is played after the thumb-side instead of the pinky-side finger.
                next_fingering = fingering

            penalty_for_this_finger = penalty_update(penalty)

            best_known_penalty = aux(last_added_note=next_note,
                                     remaining_notes=next_remaining_notes,
                                     last_added_finger=next_possible_finger,
                                     fingering=next_fingering, penalty=penalty_for_this_finger,
                                     best_known_penalty=best_known_penalty)

        return best_known_penalty

    ##End aux
    best_penalty_for_whole_scale = None
    for pinky_side_finger in (5, 4, 3, 2):
        best_penalty_for_whole_scale = aux(last_added_note=pink_side_tonic, remaining_notes=other_notes,
                                           last_added_finger=pinky_side_finger,
                                           fingering=Fingering(for_right_hand=for_right_hand).add_pinky_side(
                                               fundamental, pinky_side_finger),
                                           penalty=Penalty(), best_known_penalty=best_penalty_for_whole_scale)
    return best_penalty_for_whole_scale


class TestScalesGenerate(unittest.TestCase):
    maxDiff = None

    def generation_helper(self, fundamental: Note, scale_pattern: ScalePattern, for_right_hand: bool,
                          expected: Fingering,
                          show: bool = False):
        penalty = generate_fingering(fundamental=fundamental, scale_pattern=scale_pattern,
                                     for_right_hand=for_right_hand)
        fingering = penalty.fingering
        if show:
            scale = fingering.generate(first_played_note=fundamental, number_of_octaves=2, scale_pattern=scale_pattern)
            lily_code = lilypond_code_for_one_hand(key="c", notes_or_chords=scale, for_right_hand=for_right_hand,
                                                   midi=False)
            prefix_path = f"{test_folder}/test_generation"
            ly_path = f"{prefix_path}.ly"
            svg_path = f"{prefix_path}.svg"
            util.delete_file_if_exists(svg_path)
            util.delete_file_if_exists(ly_path)
            cmd = compile_(lily_code, file_prefix=prefix_path, execute_lily=True, wav=False)
            cmd()

        self.assertEquals(fingering, expected)

    def test_blues_D_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(note=Note(chromatic=2, diatonic=1), finger=5).
                    add(note=Note(chromatic=0, diatonic=0), finger=4).
                    add(note=Note(chromatic=9, diatonic=5), finger=2).
                    add(note=Note(chromatic=8, diatonic=4), finger=1).
                    add(note=Note(chromatic=7, diatonic=4), finger=3).
                    add(note=Note(chromatic=5, diatonic=3), finger=2).
                    add(note=Note(chromatic=2, diatonic=1), finger=1))
        fundamental = Note(chromatic=2, diatonic=1)
        self.generation_helper(fundamental=fundamental, scale_pattern=blues, for_right_hand=True, expected=expected,
                               show=True)

    def test_pentatonic_major_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(Note.from_name("C# "), 5).
                    add(Note.from_name("A# "), 4).
                    add(Note.from_name("G# "), 3).
                    add(Note.from_name("E# "), 1).
                    add(Note.from_name("D# "), 2).
                    add(Note.from_name("C# "), 1))
        self.generation_helper(fundamental=Note.from_name("C#"), scale_pattern=pentatonic_major, for_right_hand=True,
                               expected=expected)
        # All black note

    def test_minor_seventh_arpeggio_A(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(Note.from_name("A "), 5).
                    add(Note.from_name("A "), 1).
                    add(Note.from_name("C "), 2).
                    add(Note.from_name("E "), 3).
                    add(Note.from_name("G "), 4))
        self.generation_helper(fundamental=Note.from_name("A"), scale_pattern=minor_seven.to_arpeggio_pattern(),
                               for_right_hand=True, expected=expected, show=True)

    def test_minor_melodic_right(self):
        penalty = generate_fingering(fundamental=Note(chromatic=0, diatonic=0), scale_pattern=minor_melodic,
                                     for_right_hand=True)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.right_minor_melodic_fingering,
                          fingering)

    def test_minor_melodic_left(self):
        penalty = generate_fingering(fundamental=Note(chromatic=0, diatonic=0), scale_pattern=minor_melodic,
                                     for_right_hand=False)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.left_minor_melodic_fingering,
                          fingering)

    def test_augmented_major_seventh_arpeggio_f_left(self):
        expected = (Fingering(for_right_hand=False).
                    add_pinky_side(Note.from_name("F2 "), 5).
                    add(Note.from_name("A "), 4).
                    add(Note.from_name("C# "), 3).
                    add(Note.from_name("E "), 2).
                    add(Note.from_name("F "), 1))
        self.generation_helper(Note.from_name("F2"), scale_pattern=augmented_major_seventh_chord.to_arpeggio_pattern(),
                               for_right_hand=False, show=True, expected=expected)
