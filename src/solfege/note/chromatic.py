from typing import Optional
from solfege.note.abstract import AbstractNote, AlterationOutput, FixedLengthOutput, NoteOutput, OctaveOutput
from solfege.interval.chromatic import ChromaticInterval


class ChromaticNote(AbstractNote, ChromaticInterval):
    IntervalClass = ChromaticInterval

    @staticmethod
    def from_name(name) -> "ChromaticNote":
        from solfege.note.note import Note
        return Note(name).get_chromatic()

    def get_color(self, color=True):
        """Color to print the note in lilypond"""
        return "black"

    def get_name_up_to_octave(self, alteration_output: AlterationOutput, note_output: NoteOutput, fixed_length: FixedLengthOutput):
        return self.get_note().get_name_up_to_octave(alteration_output=alteration_output, note_output=note_output, fixed_length=fixed_length)

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

    def file_name(self, clef: Optional[str] = None):
        """Return the file name without extension nor folder"""
        name = f"_{self.get_name_with_octave(
                    octave_notation=OctaveOutput.MIDDLE_IS_4,
                    alteration_output = AlterationOutput.ASCII, 
                    note_output = NoteOutput.LETTER, 
                    fixed_length = FixedLengthOutput.NO
                   )}"
        if clef is not None:
            return f"_{clef}_{name}"
        return name

    def image_file_name(self, clef: Optional[str]  = None):
        """Return the file name without folder"""
        return f"{self.file_name(clef)}.svg"

    def image_html(self, clef: Optional[str]="treble"):
        """Return the html tag for the image."""
        return f"""<img src="{self.image_file_name(clef)}"/>"""

    def is_white_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        return not self.is_black_key_on_piano()

    def is_black_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().get_number() % 12) in blacks