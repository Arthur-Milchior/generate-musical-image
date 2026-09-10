from __future__ import annotations

from typing import Optional

from instruments.piano.scales.fingering import Fingering
from instruments.piano.fingering_generation.penalty_for_scale import PenaltyForScale


class Penalty(PenaltyForScale):
    """A `PenaltyForScale` for a fingering that is not yet complete (the extremities/tonic are not known yet).

    Used while incrementally fingering a melody note-by-note (see `generate.py`'s `generate_best_fingering`),
    where the extremity-dependent part of the penalty (`_ordinal`'s use of `fingering`) can't be computed until
    the whole fingering exists; `MockFingering` stands in so those checks are simply neutral in the meantime."""
    class MockFingering(Fingering):
        """A constant fingering, so that _ordinal still works and ignore the ends"""

        def __init__(self) -> None:
            """Create a placeholder right-hand fingering with no note/tonic assigned."""
            super().__init__(for_right_hand=True)

        def avoid_this_extremity(self) -> bool:
            """Always False: extremity quality isn't judged before the fingering is complete."""
            return False

        def pinky_to_thumb(self) -> bool:
            """Always False: the pinky-to-thumb extremity check isn't judged before the fingering is complete."""
            return False

        def get_thumb_side_tonic_finger(self) -> Optional[int]:
            """Always None: the tonic/thumb-side finger isn't known before the fingering is complete."""
            return None

    def __init__(self, *args, **kwargs) -> None:
        """Create a `PenaltyForScale` using `MockFingering` as its (placeholder) `fingering`."""
        super().__init__(fingering=Penalty.MockFingering(), *args, **kwargs)
