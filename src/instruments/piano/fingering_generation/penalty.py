from __future__ import annotations

from typing import Optional

from instruments.piano.scales.fingering import Fingering
from instruments.piano.fingering_generation.penalty_for_scale import PenaltyForScale


class Penalty(PenaltyForScale):
    class MockFingering(Fingering):
        """A constant fingering, so that _ordinal still works and ignore the ends"""

        def __init__(self):
            super().__init__(for_right_hand=True)

        def avoid_this_extremity(self) -> bool:
            return False

        def pinky_to_thumb(self) -> bool:
            return False

        def get_thumb_side_tonic_finger(self) -> Optional[int]:
            return None

    def __init__(self, *args, **kwargs):
        super().__init__(fingering=Penalty.MockFingering(), *args, **kwargs)
