from solfege.note.abstract import AbstractNote
from solfege.interval.chromatic import ChromaticInterval


class ChromaticNote(AbstractNote, ChromaticInterval):
    IntervalClass = ChromaticInterval

    def get_color(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def get_name_up_to_octave(self, ascii:bool = False):
        if ascii:
            return ["C", "C_sharp", "D", "E_flat", "E", "F", "F_sharp", "G", "A_flat", "A", "B_flat", "B"][self.get_number() % 12]
        else:
            return ["C", "C#", "D", "E♭", "E", "F", "F#", "G", "A♭", "A", "B♭", "B"][self.get_number() % 12]

    def get_name_with_octave(self, ascii:bool = False):
        return f"{self.get_name_up_to_octave(ascii=ascii)}{self.get_octave(scientific_notation=True)}"

    def get_degree(self):
        return ["1", "1#", "2", "3♭", "3", "4", "4#", "5", "6♭", "6", "7♭", "7"][self.get_number() % 12]

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
        return f"_{clef}_{self.get_name_with_octave(ascii=True)}"

    def image_file_name(self, clef: str):
        """Return the file name without folder"""
        return f"{self.file_name(clef)}.svg"

    def image_html(self, clef: str="treble"):
        """Return the html tag for the image."""
        return f"""<img src="{self.image_file_name(clef)}"/>"""
