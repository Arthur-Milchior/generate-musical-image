# It should generate:
# 63 scales
# 12 note
# 2 octaves
# 4 kinds
# 3 hands
# =18144 images
# Taking 4 seconds each, it takes 20 hours
from dataclasses import dataclass, astuple
from typing import Optional, List, Callable, Tuple

from lily.Lilyable.list_piano_lilyable import ListPianoLilyable
from lily.Lilyable.piano_lilyable import LiteralPianoLilyable, lilypond_code_for_one_hand
from lily.lily import compile_
from instruments.piano.fingering_generation.penalty import Penalty
from instruments.piano.piano_note import PianoNote
from instruments.piano.fingering_generation.penalty_for_scale import PenaltyForScale
from instruments.piano.scales.fingering import Fingering
from solfege.pattern.chord.chord_pattern import minor_seven, augmented_major_seventh_chord
from solfege.value.note.note import Note
from solfege.pattern.scale.scale_pattern import ScalePattern, blues, pentatonic_major, minor_melodic
from utils.constants import test_folder
from utils.util import ensure_folder, delete_file_if_exists

lilyProgram = "lilypond "


@dataclass(frozen=True)
class BestPenaltyMelody:
    penalty: PenaltyForScale
    fingerings: List[List[PianoNote]]


def generate_best_fingering(fingered_notes: List[PianoNote], penalty_for_fingered_notes: PenaltyForScale,
                            notes_to_finger: List[Note],
                            best_known_penalty_for_full_fingering: Optional[BestPenaltyMelody], for_right_hand: bool,
                            add_penalty_for_whole: Callable[
                                [List[PianoNote], PenaltyForScale], Optional[PenaltyForScale]] = (
                                    lambda fingering, p: p),
                            potential_finger_for_next_note: Optional[int] = None) -> \
        Optional[BestPenaltyMelody]:
    """
    We return a list of fingerings for fingered_notes+notes_to_finger.
    We assume no two successive notes are equal.
    Those fingerings all have the same penalty, and it is as low as possible.
    When the whole fingering is generated, add_penalty_for_whole add a `whole_penalty` to the result.
    If we can generate fingering so that their penalty+base_penalty+whole_penalty is better than best_known_penalty, then we return those fingerings.
    Otherwise, if we can generate as good as best_known_penalty, then best_known_penalty plus those fingerings.
    Otherwise, best_known_penalty.

    The finger for the first note is restricted to a note in `potential_finger_for_first_note` if it is not None, to a finger compatible with finger of last note if it exists, otherwise any finger

    this function takes ownership of best_known_penalty_for_full_fingering and of no other function.
    """
    if not notes_to_finger:
        whole_penalty = add_penalty_for_whole(fingered_notes, penalty_for_fingered_notes)
        if whole_penalty is None:
            return best_known_penalty_for_full_fingering
        if best_known_penalty_for_full_fingering is None or best_known_penalty_for_full_fingering.penalty > whole_penalty:
            return BestPenaltyMelody(whole_penalty, [fingered_notes])
        if best_known_penalty_for_full_fingering.penalty < whole_penalty:
            return best_known_penalty_for_full_fingering
        # we can't use == because this would take fingering into consideration
        best_known_penalty_for_full_fingering.fingerings.append(fingered_notes)
        return best_known_penalty_for_full_fingering

    next_note = notes_to_finger[0]

    if potential_finger_for_next_note is None:
        if fingered_notes:
            last_note = fingered_notes[-1]
            potential_finger_for_next_note = last_note.valid_next_fingers(next_note, for_right_hand=for_right_hand)
        else:
            potential_finger_for_next_note = list(range(1, 6))

    for finger in potential_finger_for_next_note:
        next_piano_note = PianoNote.make(chromatic=next_note.get_chromatic().value,
                                    diatonic=next_note.get_diatonic().value, finger=finger)
        penalty_with_note = penalty_for_fingered_notes.add_penalty_for_note(next_piano_note)
        if fingered_notes:
            last_note = fingered_notes[-1]
            penalty_with_note = penalty_with_note.add_penalty_for_note_transition(next_piano_note, last_note,
                                                                                  for_right_hand)
            if penalty_with_note is None:
                continue
        if best_known_penalty_for_full_fingering and penalty_with_note > best_known_penalty_for_full_fingering.penalty:
            # Penalty is already worse than what we can achieve, no point working more
            continue
        best_known_penalty_for_full_fingering = generate_best_fingering(
            fingered_notes=fingered_notes + [next_piano_note], penalty_for_fingered_notes=penalty_with_note,
            notes_to_finger=notes_to_finger[1:],
            best_known_penalty_for_full_fingering=best_known_penalty_for_full_fingering, for_right_hand=for_right_hand,
            add_penalty_for_whole=add_penalty_for_whole)
    return best_known_penalty_for_full_fingering


def generate_best_fingering_for_melody(notes_to_finger: List[Note],
                                       for_right_hand: bool,
                                       potential_finger_for_next_note: Optional[int] = None) -> \
        Optional[BestPenaltyMelody]:
    return generate_best_fingering(fingered_notes=[], penalty_for_fingered_notes=Penalty(),
                                   notes_to_finger=notes_to_finger,
                                   best_known_penalty_for_full_fingering=None, for_right_hand=for_right_hand,
                                   potential_finger_for_next_note=potential_finger_for_next_note)


@dataclass(frozen=True)
class BestPenaltyScale:
    penalty: PenaltyForScale
    fingerings: List[Tuple[List[PianoNote], Fingering]]

    def __iter__(self):
        return iter(astuple(self))


def generate_best_fingering_for_scale(scale: List[Note], for_right_hand: bool) -> Optional[BestPenaltyScale]:
    """Returns the best penalty that could be generated for this scale.
     scale: the list of note, from low to high, with last note an octave above the first one
     """
    assert scale[0].in_base_octave() == scale[-1].in_base_octave()

    def penalty_scale(notes: List[PianoNote], penalty: PenaltyForScale) -> Optional[PenaltyForScale]:
        fingering = FingeringSymbol.from_scale(notes, for_right_hand)
        if fingering is None:
            return None
        if for_right_hand:
            pinky_side_note = notes[-1]
            second_to_pinky_side_note = notes[-2]
            thumb_side_note = notes[0]
        else:
            pinky_side_note = notes[0]
            second_to_pinky_side_note = notes[1]
            thumb_side_note = notes[-1]
        repetition_note = PianoNote.make(chromatic=pinky_side_note.get_chromatic().value,
                                    diatonic=pinky_side_note.get_diatonic().value, finger=thumb_side_note.finger)
        penalty = penalty.add_penalty_for_note_transition(repetition_note, second_to_pinky_side_note, for_right_hand)
        if penalty:
            penalty.fingering = fingering
        return penalty

    best_penalty = generate_best_fingering(fingered_notes=[], penalty_for_fingered_notes=PenaltyForScale(),
                                           notes_to_finger=scale, best_known_penalty_for_full_fingering=None,
                                           for_right_hand=for_right_hand, add_penalty_for_whole=penalty_scale)
    if best_penalty is None:
        return None
    fingerings = [(fingering, FingeringSymbol.from_scale(fingering, for_right_hand)) for fingering in best_penalty.fingerings]
    return BestPenaltyScale(best_penalty.penalty, fingerings)


