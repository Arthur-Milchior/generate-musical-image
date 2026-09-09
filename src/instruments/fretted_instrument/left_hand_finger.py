from dataclasses import dataclass


@dataclass(frozen=True)
class LeftHandFinger:
    """Placeholder for a future left-hand-finger abstraction (1=index, ..., 4=pinky).

    Currently unused and unreferenced elsewhere in the codebase: finger numbers are represented as plain `int`s
    (see `AbstractFrettedInstrument.finger_to_fret_delta_chord`/`_scale`) and as `FingersType` (a frozenset of
    candidate finger numbers) on `PositionOnFrettedInstrumentWithFingers`
    (`instruments/fretted_instrument/position/fretted_instrument_position_with_fingers.py`); this stub predates
    that approach and has no fields yet.
    """
    pass