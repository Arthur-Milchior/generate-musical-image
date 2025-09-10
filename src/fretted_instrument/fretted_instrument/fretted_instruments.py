from fretted_instrument.fretted_instrument.fretted_instrument import FrettedInstrument
from solfege.value.note.clef import Clef

finger_to_fret_delta = {
    0: {
        1: (-1, 1),
        2: (-1, 2),
        3: (0, 2),
        4: (0, 3),
    },
    1: {
        2: (0, 1),
        3: (0, 2),
        4: (0, 3),
    },
    2: {
        3: (0, 1),
        4: (0, 2),
    },
    3: {
        4: (0, 2),
    },
    4: {},
}

ukulele_finger_to_fret_delta = {
    0: {
        1: (-2, 3),
        2: (-1, 4),
        3: (0, 4),
        4: (0, 5),
    },
    1: {
        2: (0, 2),
        3: (0, 4),
        4: (0, 6),
    },
    2: {
        3: (0, 2),
        4: (0, 4),
    },
    3: {
        4: (0, 3),
    },
    4: {},
}

# finger_to_fret_delta_hard = {
#     0: {
#         1: FretDelta(-2, 2),
#         2: FretDelta(-1, 3),
#         3: FretDelta(-1, 3),
#         4: FretDelta(-1, 3),
#     },
#     1: {
#         2: FretDelta(0, 2),
#         3: FretDelta(0, 3),
#         4: FretDelta(0, 4),
#     },
#     2: {
#         3: FretDelta(0, 2),
#         4: FretDelta(0, 3),
#     },
#     3: {
#         4: FretDelta(0, 2),
#     },
#     4: {},
# }


Ukulele = FrettedInstrument.make(
    name= "ukulele",
    number_of_frets=12, 
    open_string_chromatic_note= ["G4", "C4", "E4", "A4"],
    clef=Clef.TREBLE, 
    finger_to_fret_delta=ukulele_finger_to_fret_delta,
    )
Gui_tar = FrettedInstrument.make(
    name="fretted_instrument",
    number_of_frets=24, 
    open_string_chromatic_note= ["E3", "A3", "D4", "G4", "B4", "E5"],
    clef=Clef.TREBLE,
    finger_to_fret_delta=finger_to_fret_delta,
    )
Bass = FrettedInstrument.make(
    name = "bass",
    number_of_frets=20, 
    open_string_chromatic_note= ["E2", "A2", "D3", "G3"],
    clef=Clef.BASS,
    finger_to_fret_delta=finger_to_fret_delta,
    )

fretted_instruments = [Ukulele, Gui_tar, Bass]