from solfege.note.abstract import AbstractNote
from solfege.interval.chromatic import ChromaticInterval


class ChromaticNote(AbstractNote, ChromaticInterval):
    IntervalClass = ChromaticInterval

    def get_color(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def get_name_up_to_octave(self):
        return ["C", "C#", "D", "E♭", "E", "F", "F#", "G", "A♭", "A", "B♭", "B"][self.get_number() % 12]

    def get_note(self, cls=None):
        """A solfège note. Diatonic note is guessed. The default class is
        Note. May return None if no diatonic note can be guessed. """
        diatonic = self.get_diatonic()
        if diatonic is None:
            return None
        if cls is None:
            from solfege.note.note import Note
            cls = Note
        diatonic = diatonic.get_number()
        chromatic = self.get_number()
        return cls(diatonic=diatonic, chromatic=chromatic)

    def file_name(self, clef: str):
        """Return the file name without extension nor folder"""
        return f"_{clef}_{self.get_ascii_name(fixed_length=False)}"

    def image_file_name(self, clef: str):
        """Return the file name without extension nor folder"""
        return f"{self.file_name(clef)}.svg"

    def image_html(self, clef: str="treble"):
        """Return the file name without extension nor folder"""
        return f"""<img src="{self.image_file_name(clef)}"/>"""
