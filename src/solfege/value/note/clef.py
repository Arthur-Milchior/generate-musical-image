from enum import StrEnum


class Clef(StrEnum):
    """Which musical staff clef to use when rendering a note."""
    TREBLE = "treble"
    """The treble (G) clef, used for higher-pitched notes."""
    BASS = "bass"
    """The bass (F) clef, used for lower-pitched notes."""