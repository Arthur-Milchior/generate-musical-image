# It should generate:
# 63 scales
# 12 note
# 2 octaves
# 4 kinds
# 3 hands
# =18144 images
# Taking 4 seconds each, it takes 20 hours
import unittest
from typing import Optional, List

from piano.Fingering.fingering import Fingering, TestFingering
from piano.Fingering.penalty import Penalty
from piano.pianonote import PianoNote
from solfege.Scale.pattern import ScalePattern, minor_melodic, blues
from solfege.interval.interval import Interval

lilyProgram = "lilypond "


def generate_fingering(tonic: PianoNote, scale: ScalePattern, for_right_hand: bool,
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

    def aux(current_note: PianoNote, remaining_intervals: List[Interval], current_finger: int, fingering: Fingering) -> \
            Optional[Penalty]:
        """
        Return the best extension of `fingering`, with `current_note` associated to `current_finger`.
        The extension should be valid for the notes
        * current_note
        * current_note + remaining_intervals[0]
        * current_note + remaining_intervals[0] + remaining_intervals[1]
         and so on, for the left hand.
         and in reverse for the right hand.

         Return the best penalty if it exists.
        """

        if current_note.is_black() and current_finger == 1:
            return None

        next_fingering = fingering.add(current_note, current_finger)
        if next_fingering is False:
            # Another finger is associated to this note (up to octave, and not including the starting finger)
            return None
        if next_fingering is True:
            # This association is already in the Fingering.
            next_fingering = fingering
        if not remaining_intervals:
            thumb_side_tonic_finger = next_fingering.get_thumb_side_tonic_finger()
            nice_extremity = next_fingering.is_end_nice()
            return Penalty(thumb_side_tonic_finger=thumb_side_tonic_finger, nice_extremity=nice_extremity,
                           fingering=next_fingering)

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

        next_note = current_note + next_interval
        local_penalty = Penalty()
        if current_finger == 1:
            if not tonic.equals_modulo_octave(current_note):
                local_penalty = local_penalty.add_passing_finger()
            if not current_note.adjacent(next_note):
                local_penalty = local_penalty.add_thumb_non_adjacent()
            if not next_note.is_black():
                local_penalty = local_penalty.add_white_after_thumb()
            next_possible_fingers = [3, 4, 2]
        elif current_finger == 2:
            next_possible_fingers = [1]
        elif current_note.adjacent(next_note):
            next_possible_fingers = [current_finger - 1]
        else:
            next_possible_fingers = [current_finger - 1, current_finger - 2]

        best_penalty: Optional[Penalty] = None
        for next_possible_finger in next_possible_fingers:
            best_penalty_for_next_possible_finger = aux(current_note=next_note,
                                                        remaining_intervals=next_remaining_intervals,
                                                        current_finger=next_possible_finger, fingering=next_fingering)
            if best_penalty_for_next_possible_finger is None:
                continue
            best_fingering_for_next_possible_finger = best_penalty_for_next_possible_finger.fingering
            sum_penalty = best_penalty_for_next_possible_finger + local_penalty
            sum_penalty.fingering = best_fingering_for_next_possible_finger
            if best_penalty is None or sum_penalty < best_penalty:
                best_penalty = sum_penalty
        return best_penalty

    ##End aux
    best_penalty = None
    for pinky_side_first_finger in (2, 3, 4, 5):
        best_penalty_for_this_first_finger = aux(current_note=tonic, remaining_intervals=intervals,
                                                 current_finger=pinky_side_first_finger, fingering=fingering)
        if best_penalty_for_this_first_finger is None:
            continue
        best_fingering_for_this_first_finger = best_penalty_for_this_first_finger.fingering
        penalty = best_penalty_for_this_first_finger.add_starting_finger(pinky_side_first_finger,
                                                                         fingering=best_fingering_for_this_first_finger)
        if best_penalty is None or penalty < best_penalty:
            best_penalty = penalty
    return best_penalty


class TestGenerate(unittest.TestCase):
    def test_blues_D_right(self):
        penalty = generate_fingering(tonic=PianoNote(diatonic=1, chromatic=2), scale=blues,
                                     for_right_hand=True)
        fingering = penalty.fingering
        expected = (Fingering(for_right_hand=True).
                    add(note=PianoNote(chromatic=2, diatonic=1), finger=5).
                    add(note=PianoNote(chromatic=0, diatonic=0), finger=4).
                    add(note=PianoNote(chromatic=9, diatonic=5), finger=3).
                    add(note=PianoNote(chromatic=8, diatonic=4), finger=2).
                    add(note=PianoNote(chromatic=7, diatonic=4), finger=1).
                    add(note=PianoNote(chromatic=5, diatonic=3), finger=3).
                    add(note=PianoNote(chromatic=2, diatonic=1), finger=1))
        self.assertEquals(fingering, expected)

    def test_minor_melodic_right(self):
        penalty = generate_fingering(tonic=PianoNote(diatonic=0, chromatic=0), scale=minor_melodic,
                                     for_right_hand=True)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.right_minor_melodic_fingering,
                          fingering)

    def test_minor_melodic_left(self):
        penalty = generate_fingering(tonic=PianoNote(diatonic=0, chromatic=0), scale=minor_melodic,
                                     for_right_hand=False)
        fingering = penalty.fingering
        self.assertEquals(TestFingering.left_minor_melodic_fingering,
                          fingering)
