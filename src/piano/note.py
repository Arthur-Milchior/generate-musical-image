import solfege.note


class Note(solfege.note.Note):
    """Represents a note on the keyboard."""
    def adjacent(self, other):
        """Whether `other` is at most two half-tone away"""
        return abs(other.get_number() - self.get_number()) <= 2

    def is_black(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.getChromatic().get_number() % 12) in blacks


#twelve_notes = [(Note(toCopy=note), nbBemol) for note, nbBemol in solfege.note.twelve_notes]
