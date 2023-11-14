# It should generate:
# 63 scales
# 12 note
# 2 octaves
# 4 kinds
# 3 hands
# =18144 images
# Taking 4 seconds each, it takes 20 hours
from typing import Optional, List

import util
from piano.Fingering.container import Fingering
from piano.Fingering.penalty import Penalty
from piano.pianonote import PianoNote
from solfege.interval.interval import Interval

lilyProgram = "lilypond "


def generate_left_fingering_dic(currentNote: PianoNote, intervals: List[Interval],
                                fingering_dic: Optional[Fingering] = None):
    util.debug("Generating left fingering for %s", currentNote.get_interval_name())
    # repeating last interval so that we ensure we can go on second octave of the scale even if first and last finger
    # are different.
    intervals = intervals + [intervals[0]]
    return generate_fingering_dic(currentNote, intervals, False, fingering=fingering_dic)


def generate_right_fingering_dic(currentNote: PianoNote, intervals: List[Interval],
                                 fingering_dic: Optional[Fingering] = None):
    # repeating last interval so that we ensure we can go on second octave of the scale even if first and last finger
    # are different.
    intervals = [intervals[-1]] + intervals
    return generate_fingering_dic(currentNote, intervals, True, fingering=fingering_dic)


def generate_fingering_dic(base_note: PianoNote, intervals: List[Interval], is_right: bool,
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
        fingering = Fingering()

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
            ending_finger = next_fingering.get_last_finger()
            nice_extremity = next_fingering.is_end_nice()
            return Penalty(ending_finger=ending_finger, nice_extremity=nice_extremity, fingering=next_fingering)

        # on the right hand, we go from high to low. So we take the last interval and reverse it to decrease the
        # current note.
        # On the left hand, we go from low to high, so we take the first interval and use it to increase the
        # current note.
        next_interval = remaining_intervals[-1 if is_right else 0]
        if is_right:
            next_interval = -next_interval
            next_remaining_intervals = remaining_intervals[:-1]
        else:
            next_remaining_intervals = remaining_intervals[1:]

        next_note = current_note + next_interval
        local_penalty = Penalty()
        if current_finger == 1:
            if not base_note.equals_modulo_octave(current_note):
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
    for starting_finger in reversed(range(1, 6)):
        best_penalty_for_starting_finger = aux(current_note=base_note, remaining_intervals=intervals,
                                               current_finger=starting_finger, fingering=fingering)
        if best_penalty_for_starting_finger is None:
            continue
        best_fingering_for_starting_finger = best_penalty_for_starting_finger.fingering
        penalty = best_penalty_for_starting_finger.add_starting_finger(starting_finger,
                                                                       fingering=best_fingering_for_starting_finger)
        if best_penalty is None or penalty < best_penalty:
            best_penalty = penalty
    return best_penalty


def generate_left_fingering(starting_finger: int, fingering: Fingering, base_note: PianoNote, intervals: List[Interval],
                            nbOctave: int = 1):
    intervals = intervals * nbOctave
    first_interval = intervals[0]
    next_intervals = intervals[1:]
    # Lowering the scale by an octave or two so that it's easier to play on left hand on piano
    base_note = base_note.add_octave(-1 if nbOctave == 1 else -2)
    next_note = base_note + first_interval
    return [(base_note, starting_finger)] + generate_fingering(next_note, next_intervals, fingering)


def generate_right_fingering(starting_finger: int, fingering: Fingering, base_note: PianoNote, intervals: List[Interval],
                             nbOctave: int = 1):
    end_note = base_note.add_octave(nbOctave)
    intervals = intervals * nbOctave
    intervals = intervals[:-1]
    return generate_fingering(base_note, intervals, fingering) + [(end_note, starting_finger)]


def generate_fingering(currentNote: PianoNote, remainingInterval: List[Interval], fingering: Fingering):
    l = []
    for nextInterval in remainingInterval + [None]:  # adding a last element so the loop is processed once more
        finger = fingering.get_finger(currentNote)
        l.append((currentNote, finger))
        if nextInterval:
            currentNote += nextInterval
    return l
