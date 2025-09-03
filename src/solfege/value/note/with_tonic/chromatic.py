
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Union
from solfege.value.note.chromatic_note import ChromaticNote
from solfege.value.note.with_tonic.singleton import AbstractSingletonNoteWithTonic

@dataclass(frozen=True, eq=False)
class ChromaticNoteWithTonic(AbstractSingletonNoteWithTonic, ChromaticNote):
    # The role this note is most likely to play in the standard chords
    # Especially used for guitar cards
    role: ClassVar[List[Optional[str]]] = ["unison", None, None, "third", "third", "third", "fifth", "fifth", "fifth", "interval", "interval",
            "interval"]

    def get_color(self, color=True):
        """Coloring for guitar dots."""
        if color:
            dic = {"unison": "black", "third": "violet", "fifth": "red", "interval": "green", None: None}
            return dic[self.get_role()]
        else:
            return "black"


