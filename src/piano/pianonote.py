from typing import Optional

import solfege.note


class PianoNote(solfege.note.Note):
    """Represents a note on the keyboard."""

    def __init__(self, finger: Optional[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.finger = finger

    def adjacent(self, other):
        """Whether `other` is at most two half-tone away"""
        return abs(other.get_number() - self.get_number()) <= 2

    def is_black(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().get_number() % 12) in blacks

# twelve_notes = [(Note(toCopy=note), nbBemol) for note, nbBemol in solfege.note.twelve_notes]
