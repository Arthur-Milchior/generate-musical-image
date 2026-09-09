from enum import Enum

class Playable(Enum):
    """How playable a chord fingering is, as determined by `HandForChordForFrettedInstrument.playable`/
    `ChordOnFrettedInstrument.playable`."""

    EASY = "EASY"
    """The fingering is playable without any unusual finger stretch."""
    YES = "YES"
    """Reserved for a harder-but-still-playable tier; not currently produced by any code in this package (only
    `EASY` and `NO` are returned today)."""
    NO = "NO"
    """The fingering isn't playable (some pair of fingers is spread further than the instrument allows)."""