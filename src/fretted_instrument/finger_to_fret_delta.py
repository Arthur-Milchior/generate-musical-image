from fretted_instrument.position.fret.fret_deltas import FretDelta


finger_to_fret_delta = {
    0: {
        1: FretDelta(-1, 1),
        2: FretDelta(-1, 2),
        3: FretDelta(0, 2),
        4: FretDelta(0, 3),
    },
    1: {
        2: FretDelta(0, 1),
        3: FretDelta(0, 2),
        4: FretDelta(0, 3),
    },
    2: {
        3: FretDelta(0, 1),
        4: FretDelta(0, 2),
    },
    3: {
        4: FretDelta(0, 2),
    },
    4: {},
}

finger_to_fret_delta_hard = {
    0: {
        1: FretDelta(-2, 2),
        2: FretDelta(-1, 3),
        3: FretDelta(-1, 3),
        4: FretDelta(-1, 3),
    },
    1: {
        2: FretDelta(0, 2),
        3: FretDelta(0, 3),
        4: FretDelta(0, 4),
    },
    2: {
        3: FretDelta(0, 2),
        4: FretDelta(0, 3),
    },
    3: {
        4: FretDelta(0, 2),
    },
    4: {},
}

for lower in range(4):
    for higher in range (lower+1, 5):
        finger_to_fret_delta[higher][lower] = -finger_to_fret_delta[lower][higher]
        finger_to_fret_delta_hard[higher][lower] = -finger_to_fret_delta_hard[lower][higher]