from solfege.interval.alteration import Alteration

LILY = "LILY"
FILE_NAME = "FILE_NAME"
TEXT = "TEXT"
MONOSPACE = "MONOSPACE"


class Alteration(Alteration):
    def lily(self):
        """Text to obtain this alteration in Lilypond"""
        return ["eses", "es", "", "is", "isis"][self.get_number() + 2]

    def get_note_name(self, usage: str):
        """The name of this note.

        Args: `for_file` -- whether we should avoid non ascii symbol"""
        if usage == MONOSPACE:
            return ["♭♭", "♭ ", "  ", "# ", "𝄪 "][self.get_number() + 2]
        if usage == TEXT:
            return ["♭♭", "♭", "", "#", "𝄪"][self.get_number() + 2]
        if usage == FILE_NAME:
            return [
                "double_flat",
                "flat_",
                "_____",
                "sharp",
                "double_sharp",
            ][self.get_number() + 2]
        assert usage == LILY
        return self.lily()
