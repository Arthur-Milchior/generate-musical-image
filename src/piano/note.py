import solfege.note


class Note(solfege.note.Note):
    def adjacent(self, other):
        return abs(other.get_number() - self.getNumber()) <= 2

    def isBlack(self):
        blacks = {1, 3, 6, 8, 10}
        return (self.getChromatic().get_number() % 12) in blacks


twelve_notes = [(Note(toCopy=note), nbBemol) for note, nbBemol in solfege.note.twelve_notes]
