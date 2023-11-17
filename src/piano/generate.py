# It should generate:
# 63 scales
# 12 note
# 2 octaves
# 4 kinds
# 3 hands
# =18144 images
# Taking 4 seconds each, it takes 20 hours
import unittest
from typing import Optional, List, Tuple, Union, Callable

from piano.Fingering.fingering import Fingering, TestFingering
from piano.Fingering.penalty import Penalty
from piano.pianonote import PianoNote
from solfege.Scale.pattern import ScalePattern, minor_melodic, blues
from solfege.interval.interval import Interval
from solfege.note import Note

lilyProgram = "lilypond "


def generate_fingering(tonic: Note, scale: ScalePattern, for_right_hand: bool,
                       fingering: Optional[Fingering] = None) -> Optional[Penalty]:
    """
    Returns the best penalty extending `fingering` to add `base_note`, and then one note per interval starting at
    `base_note`.

    For the left hand, the notes added are thus:
    * base_note
    * base_note + intervals[0]
    * base_note + intervals[0] + intervals[1]
     that is, the generation starts from the side of the pinky finger, from the lowest note, up to the thumb/higher
     note. On the right hand it is the reverse.

    return False if no fingering can be found
    Otherwise, return:
       --the starting finger (lowest for left hand, highest for right hand),
       --the fingering for the non-starting notes
       , and
       --the penalty
    """

    if fingering is None:
        fingering = Fingering(for_right_hand=for_right_hand)
    intervals = scale.get_intervals()
    if for_right_hand:
        # We want the scale to be able to continue after the lowest note, after the thumb_over, so adding a last
        # interval
        intervals = [intervals[-1]] + intervals
    else:
        # We want the scale to be able to continue after the highest note, after the thumb_over, so adding a last
        # interval
        intervals = intervals + [intervals[0]]

    def aux(last_added_note: Note, remaining_intervals: List[Interval], last_added_finger: int, fingering: Fingering,
            penalty: Penalty) -> Optional[Penalty]:
        """
        Return the best extension of `fingering`, with `current_note` associated to `current_finger`.
        Penalty -- the penalty for currently added fingers, not considering penalties associated to extrimities.
        The extension should be valid for the notes
        * current_note
        * current_note + remaining_intervals[0]
        * current_note + remaining_intervals[0] + remaining_intervals[1]
         and so on, for the left hand.
         and in reverse for the right hand.

         Return the best penalty if it exists.
        """
        if not remaining_intervals:
            penalty = penalty.set_extremity(fingering.is_end_nice())
            penalty.thumb_side_tonic_finger = fingering.get_thumb_side_tonic_finger()
            penalty.fingering = fingering
            # it's okay to edit in place as `penalty` is a local variable that has no other owner
            return penalty

        # on the right hand, we go from high to low. So we take the last interval and reverse it to decrease the
        # current note.
        # On the left hand, we go from low to high, so we take the first interval and use it to increase the
        # current note.
        next_interval = remaining_intervals[-1 if for_right_hand else 0]
        if for_right_hand:
            next_interval = -next_interval
            next_remaining_intervals = remaining_intervals[:-1]
        else:
            next_remaining_intervals = remaining_intervals[1:]

        next_note = last_added_note + next_interval

        # List of possible next finger, and potentially the way the Penalty would change using it
        next_possible_fingers: List[Union[int, Tuple[int, Callable[[Penalty], Penalty]]]]
        if last_added_finger == 1:
            if not tonic.equals_modulo_octave(last_added_note):
                penalty = penalty.add_passing_finger()
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

        best_penalty: Optional[Penalty] = None
        for next_possible_finger in next_possible_fingers:
            if isinstance(next_possible_finger, tuple):
                next_possible_finger, penalty_update = next_possible_finger
            else:
                assert isinstance(next_possible_finger, int)
                penalty_update = lambda penalty: penalty

            if last_added_note.is_black_key_on_piano() and last_added_finger == 1:
                continue
            next_fingering = fingering.add(next_note, next_possible_finger)
            if next_fingering is False:
                # Another finger is associated to this note (up to octave, and not including the starting finger)
                continue
            if next_fingering is True:
                # This association is already in the Fingering.
                # It should only occur in the second time we consider the second note of the scale
                # when this note is played after the thumb-side instead of the pinky-side finger.
                next_fingering = fingering

            best_penalty_for_next_possible_finger = aux(last_added_note=next_note,
                                                        remaining_intervals=next_remaining_intervals,
                                                        last_added_finger=next_possible_finger,
                                                        fingering=next_fingering, penalty=penalty)
            if best_penalty_for_next_possible_finger is None:
                continue
            best_penalty_for_next_possible_finger = penalty_update(best_penalty_for_next_possible_finger)
            if best_penalty is None or best_penalty_for_next_possible_finger < best_penalty:
                best_penalty = best_penalty_for_next_possible_finger

        return best_penalty

    ##End aux
    best_penalty_for_whole_scale = None
    for pinky_side_first_finger in (5, 4, 3, 2):
        best_penalty_for_this_first_finger = aux(last_added_note=tonic, remaining_intervals=intervals,
                                                 last_added_finger=pinky_side_first_finger,
                                                 fingering=fingering.add_pinky_side(tonic, pinky_side_first_finger),
                                                 penalty=Penalty())
        if best_penalty_for_this_first_finger is None:
            continue
        penalty = best_penalty_for_this_first_finger.add_starting_finger(pinky_side_first_finger)
        if best_penalty_for_whole_scale is None or penalty < best_penalty_for_whole_scale:
            best_penalty_for_whole_scale = penalty
    return best_penalty_for_whole_scale


class TestGenerate(unittest.TestCase):
    maxDiff = None
    def test_blues_D_right(self):
        penalty = generate_fingering(tonic=Note(chromatic=2, diatonic=1), scale=blues,
                                     for_right_hand=True)
        fingering = penalty.fingering
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(note=Note(chromatic=2, diatonic=1), finger=4).
                    add(note=Note(chromatic=0, diatonic=0), finger=3).
                    add(note=Note(chromatic=9, diatonic=5), finger=1).
                    add(note=Note(chromatic=8, diatonic=4), finger=4).
                    add(note=Note(chromatic=7, diatonic=4), finger=3).
                    add(note=Note(chromatic=5, diatonic=3), finger=2).
                    add(note=Note(chromatic=2, diatonic=1), finger=1))
        self.assertEquals(fingering, expected)

    def test_minor_melodic_right(self):
        penalty = generate_fingering(tonic=Note(chromatic=0, diatonic=0), scale=minor_melodic,
                                     for_right_hand=True)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.right_minor_melodic_fingering,
                          fingering)

    def test_minor_melodic_left(self):
        penalty = generate_fingering(tonic=Note(chromatic=0, diatonic=0), scale=minor_melodic,
                                     for_right_hand=False)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.left_minor_melodic_fingering,
                          fingering)
