from typing import List, Optional
from instruments.fretted_instrument.fretted_instrument.abstract_fretted_instrument import AbstractFrettedInstrument
from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.fretted_instrument.tuning import Tuning
from instruments.fretted_instrument.position.fret.fret_delta import FretDelta
from solfege.value.note.clef import Clef
from utils.util import assert_typing

finger_to_fret_delta = {
    0: {
        1: FretDelta((-1, 1)),
        2: FretDelta((-1, 2)),
        3: FretDelta((0, 2)),
        4: FretDelta((0, 3)),
    },
    1: {
        2: FretDelta((0, 1)),
        3: FretDelta((0, 2)),
        4: FretDelta((0, 3)),
    },
    2: {
        3: FretDelta((0, 1)),
        4: FretDelta((0, 2)),
    },
    3: {
        4: FretDelta((0, 2)),
    },
    4: {},
}

ukulele_finger_to_fret_delta = {
    0: {
        1: FretDelta((-2, 3)),
        2: FretDelta((-1, 4)),
        3: FretDelta((0, 4)),
        4: FretDelta((0, 5)),
    },
    1: {
        2: FretDelta((0, 2)),
        3: FretDelta((0, 4)),
        4: FretDelta((0, 6)),
    },
    2: {
        3: FretDelta((0, 2)),
        4: FretDelta((0, 4)),
    },
    3: {
        4: FretDelta((0, 3)),
    },
    4: {},
}

for lower, dic in ukulele_finger_to_fret_delta.items():
    for higher, delta in dic.items():
        assert_typing(delta, FretDelta)

# finger_to_fret_delta_hard = {
#     0: {
#         1: FretDelta((-2, 2)),
#         2: FretDelta((-1, 3)),
#         3: FretDelta((-1, 3)),
#         4: FretDelta((-1, 3)),
#     },
#     1: {
#         2: FretDelta((0, 2)),
#         3: FretDelta((0, 3)),
#         4: FretDelta((0, 4)),
#     },
#     2: {
#         3: FretDelta((0, 2)),
#         4: FretDelta((0, 3)),
#     },
#     3: {
#         4: FretDelta((0, 2)),
#     },
#     4: {},
# }


abstract_ukulele = AbstractFrettedInstrument.make(
    _name= "ukulele",
    number_of_frets=12, 
    clef=Clef.TREBLE, 
    finger_to_fret_delta=ukulele_finger_to_fret_delta,
    number_of_strings = 4,
    number_of_scales_reachable_per_string = [0, 1, 0, 0],
    )
ukulele_tuning = Tuning.make(["G4", "C4", "E4", "A4"])
Ukulele = FrettedInstrument(abstract_ukulele, ukulele_tuning)

abstract_bass = AbstractFrettedInstrument.make(
    _name = "bass",
    number_of_frets=20, 
    clef=Clef.BASS,
    finger_to_fret_delta=finger_to_fret_delta,
    number_of_strings = 4,
    number_of_scales_reachable_per_string = [1, 1, 0, 0],
    )
bass_tuning = Tuning.make(["E2", "A2", "D3", "G3"])
Bass = FrettedInstrument(abstract_bass, bass_tuning)

abstract_guitar = AbstractFrettedInstrument.make(
        _name="guitar",
        number_of_frets=24, 
        clef=Clef.TREBLE,
        finger_to_fret_delta=finger_to_fret_delta,
        number_of_strings = 6,
        number_of_scales_reachable_per_string = [2, 2, 1, 1, 0, 0],
    )
guitar_default_tuning = Tuning.make(["E3", "A3", "D4", "G4", "B4", "E5"])
 
Guitar  = FrettedInstrument(abstract_guitar, guitar_default_tuning)
drop_d = Tuning.make(["D3", "A3", "D4", "G4", "B4", "E5"], "drop D")
double_drop_d = Tuning.make(["D3", "A3", "D4", "G4", "B4", "E5"], "Douple drop d")
vestapol = Tuning.make(["D3", "A3", "D4", "F4#", "A4", "D5"], "Vestapol")
english_guitar = Tuning.make(["C3", "E3", "G3", "C4", "E4", "G4"], "English Guitar")
overtone_G = Tuning.make(["G3", "G4", "D5", "G5", "B5", "D6"], "Overtone G")

fretted_instruments = [Guitar, Ukulele, Bass]

