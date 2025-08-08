
from typing import Union
from solfege.note import ChromaticNote
from solfege.note.with_tonic.base import AbstractNoteWithTonic


class ChromaticNoteWithTonic(AbstractNoteWithTonic, ChromaticNote):
    # The role this note is most likely to play in the standard chords
    # Especially used for guitar cards
    role = ["unison", None, None, "third", "third", "third", "fifth", "fifth", "fifth", "interval", "interval",
            "interval"]

    def get_color(self, color=True):
        if color:
            dic = {"unison": "black", "third": "violet", "fifth": "red", "interval": "green", None: None}
            return dic[self.get_role()]
        else:
            return "black"


