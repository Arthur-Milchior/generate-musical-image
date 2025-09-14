from instruments.fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from instruments.fretted_instrument.position.fret.fret_deltas import FretDelta
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


Ukulele = FrettedInstrument.make(
    name= "ukulele",
    number_of_frets=12, 
    open_string_chromatic_note= ["G4", "C4", "E4", "A4"],
    clef=Clef.TREBLE, 
    finger_to_fret_delta=ukulele_finger_to_fret_delta,
    number_of_scales_reachable_per_string = [0, 1, 0, 0],
    )
Guitar = FrettedInstrument.make(
    name="guitar",
    number_of_frets=24, 
    open_string_chromatic_note= ["E3", "A3", "D4", "G4", "B4", "E5"],
    clef=Clef.TREBLE,
    finger_to_fret_delta=finger_to_fret_delta,
    number_of_scales_reachable_per_string = [2, 2, 1, 1, 0, 0],
    )
Bass = FrettedInstrument.make(
    name = "bass",
    number_of_frets=20, 
    open_string_chromatic_note= ["E2", "A2", "D3", "G3"],
    clef=Clef.BASS,
    finger_to_fret_delta=finger_to_fret_delta,
    number_of_scales_reachable_per_string = [1, 1, 0, 0],
    )

fretted_instruments = [Guitar, Ukulele, Bass]