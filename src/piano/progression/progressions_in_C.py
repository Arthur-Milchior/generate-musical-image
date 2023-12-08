import unittest
from typing import List

from lily.lily import compile_
from lily.svg import display_svg_file
from piano.progression.chord_progression import TwoHandsChord, ChordProgression
from solfege.note import Note
from solfege.note.set_of_notes import SetOfNotes
from utils.constants import test_folder

C4 = Note("C4")

ii_min_7_third_and_seventh = TwoHandsChord(name="ii",
                                           left_hand=SetOfNotes([
                                            Note("D3"),
                                        ]),
                                           right_hand=SetOfNotes([
                                            Note("F4"),
                                            Note("C5"),
                                        ]),
                                           )
v_dominant_seventh_and_third = TwoHandsChord(name="V",
                                             left_hand=SetOfNotes([
                                              Note("G3"),
                                          ]),
                                             right_hand=SetOfNotes([
                                              Note("F4"),
                                              Note("B4"),
                                          ]),
                                             )
i_maj_7_third_and_seventh = TwoHandsChord(name="I",
                                          left_hand=SetOfNotes([
                                           Note("C3"),
                                       ]),
                                          right_hand=SetOfNotes([
                                           Note("E4"),
                                           Note("B4"),
                                       ]),
                                          )
ii_v_i_third_and_seventh = ChordProgression(progression_name="ii V I", disambiguation="3 7", key=C4, chords=
[ii_min_7_third_and_seventh, v_dominant_seventh_and_third,
 i_maj_7_third_and_seventh])

ii_min_7_seventh_and_third = TwoHandsChord(name="ii",
                                           left_hand=SetOfNotes([
                                            Note("D3"),
                                        ]),
                                           right_hand=SetOfNotes([
                                            Note("C5"),
                                            Note("F5"),
                                        ]),
                                           )
v_dominant_third_and_seventh = TwoHandsChord(name="V",
                                             left_hand=SetOfNotes([
                                              Note("G3"),
                                          ]),
                                             right_hand=SetOfNotes([
                                              Note("B4"),
                                              Note("F5"),
                                          ]),
                                             )
i_maj_7_seventh_and_third = TwoHandsChord(name="I",
                                          left_hand=SetOfNotes([
                                           Note("C3"),
                                       ]),
                                          right_hand=SetOfNotes([
                                           Note("B4"),
                                           Note("E5"),
                                       ]),
                                          )
ii_v_i_seventh_and_third = ChordProgression(progression_name="ii V I", disambiguation="7 3", key=C4, chords=
[ii_min_7_seventh_and_third, v_dominant_third_and_seventh,
 i_maj_7_seventh_and_third])

ii_min_7_third_fifth_and_seventh = TwoHandsChord(name="ii",
                                                 left_hand=SetOfNotes([
                                                  Note("D3"),
                                              ]),
                                                 right_hand=SetOfNotes([
                                                  Note("F4"),
                                                  Note("A4"),
                                                  Note("C5"),
                                              ]),
                                                 )
v_dominant_seventh_third_and_fifth = TwoHandsChord(name="V",
                                                   left_hand=SetOfNotes([
                                                    Note("G3"),
                                                ]),
                                                   right_hand=SetOfNotes([
                                                    Note("F4"),
                                                    Note("B4"),
                                                    Note("D5"),
                                                ]),
                                                   )
i_maj_7_fifth_seventh_and_third = TwoHandsChord(name="I",
                                                left_hand=SetOfNotes([
                                                 Note("C3"),
                                             ]),
                                                right_hand=SetOfNotes([
                                                 Note("G4"),
                                                 Note("B4"),
                                                 Note("E5"),
                                             ]),
                                                )
ii_v_i_third_fifth_and_seventh = ChordProgression(progression_name="ii V I", disambiguation="3 5 7", key=C4,
                                                  chords=[ii_min_7_third_fifth_and_seventh,
                                                          v_dominant_seventh_third_and_fifth,
                                                          i_maj_7_fifth_seventh_and_third])

ii_min_7_seventh_third_and_fifth = TwoHandsChord(name="ii",
                                                 left_hand=SetOfNotes([
                                                  Note("D3"),
                                              ]),
                                                 right_hand=SetOfNotes([
                                                  Note("C4"),
                                                  Note("F4"),
                                                  Note("A4"),
                                              ]),
                                                 )
v_dominant_fifth_seventh_and_third = TwoHandsChord(name="V",
                                                   left_hand=SetOfNotes([
                                                    Note("G3"),
                                                ]),
                                                   right_hand=SetOfNotes([
                                                    Note("D4"),
                                                    Note("F4"),
                                                    Note("B4"),
                                                ]),
                                                   )
i_maj_7_third_fifth_and_seventh = TwoHandsChord(name="I",
                                                left_hand=SetOfNotes([
                                                 Note("C3"),
                                             ]),
                                                right_hand=SetOfNotes([
                                                 Note("E4"),
                                                 Note("G4"),
                                                 Note("B4"),
                                             ]),
                                                )
ii_v_i_seventh_third_and_fifth = ChordProgression(progression_name="ii V I", disambiguation="7 3 5", key=C4,
                                                  chords=[ii_min_7_seventh_third_and_fifth,
                                                          v_dominant_fifth_seventh_and_third,
                                                          i_maj_7_third_fifth_and_seventh])

ii_min_7_fifth_seventh_and_third = TwoHandsChord(name="ii",
                                                 left_hand=SetOfNotes([
                                                  Note("D3"),
                                              ]),
                                                 right_hand=SetOfNotes([
                                                  Note("A4"),
                                                  Note("C5"),
                                                  Note("F5"),
                                              ]),
                                                 )
v_dominant_third_fifth_and_seventh = TwoHandsChord(name="V",
                                                   left_hand=SetOfNotes([
                                                    Note("G3"),
                                                ]),
                                                   right_hand=SetOfNotes([
                                                    Note("B4"),
                                                    Note("D5"),
                                                    Note("F5"),
                                                ]),
                                                   )
i_maj_7_seventh_third_and_fifth = TwoHandsChord(name="I",
                                                left_hand=SetOfNotes([
                                                 Note("C3"),
                                             ]),
                                                right_hand=SetOfNotes([
                                                 Note("B4"),
                                                 Note("E5"),
                                                 Note("G5"),
                                             ]),
                                                )
ii_v_i_fifth_seventh_and_third = ChordProgression(progression_name="ii V I", disambiguation="5 7 3", key=C4,
                                                  chords=[ii_min_7_fifth_seventh_and_third,
                                                          v_dominant_third_fifth_and_seventh,
                                                          i_maj_7_seventh_third_and_fifth])

patterns_in_C: List[ChordProgression] = [
    ii_v_i_third_and_seventh,
    ii_v_i_seventh_and_third,
    ii_v_i_third_fifth_and_seventh,
    ii_v_i_seventh_third_and_fifth,
    ii_v_i_fifth_seventh_and_third, ]


class ProgressionPatternTest(unittest.TestCase):
    maxDiff = None

    def test_see_all(self):
        for chord in patterns_in_C:
            lily = chord.lily()
            path = f"{test_folder}/{chord.progression_name.replace(' ', '_')}"
            compile_(lily, path, wav=True)
            display_svg_file(f"{path}.svg")
