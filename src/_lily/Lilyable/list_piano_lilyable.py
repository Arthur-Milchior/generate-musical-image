from dataclasses import dataclass
from typing import List, Optional

from _lily.Lilyable.piano_lilyable import PianoLilyable, LiteralPianoLilyable


@dataclass(eq=False)
class ListPianoLilyable(PianoLilyable):
    """Concatenates several `PianoLilyable`s (e.g. successive chords of a scale/progression) into one combined
    piece, inserting a `\\key` change whenever consecutive elements don't share the same key.

    Each element must have the same set of left/right/annotation (i.e. either all elements provide a given hand
    /annotation, or none do)."""
    list: List[PianoLilyable]
    """The elements to concatenate, in order."""
    separator: str = " "
    """Separator inserted between elements in the scale/annotation source code (and between bars, together with
    `bar_separator` when set)."""
    bar_separator: Optional[str] = None
    """If given, the bar-line string used inside a `\\bar "..."` marking inserted between elements; if `None`,
    elements are simply joined with `separator`."""

    def first_key(self) -> str:
        """The key of the first element, used as this combined piece's overall `first_key()`."""
        return self.list[0].first_key()

    def left_lily(self) -> Optional[str]:
        """The left-hand LilyPond code for all elements concatenated, with a `\\key` change inserted whenever an
        element's key differs from the previous one. Returns `None` if no element provides left-hand code
        (asserts that either all or none do)."""
        lefts = []
        last_key = self.first_key()
        none_found = False
        for piano_lilyable in self.list:
            lily = piano_lilyable.left_lily()
            if lily is None:
                none_found = True
                continue
            piano_lilyable_key = piano_lilyable.first_key()
            if piano_lilyable_key != last_key:
                last_key = piano_lilyable_key
                lily = f"""\\key {piano_lilyable_key} \\major{self.separator}{lily}"""
            lefts.append(lily)
        if none_found:
            assert lefts == []
            return None
        assert len(lefts) == len(self.list)
        separator = f"""\\bar "{self.bar_separator}"{self.separator}""" if self.bar_separator is not None else self.separator
        return separator.join(lefts)

    def right_lily(self) -> Optional[str]:
        """The right-hand LilyPond code for all elements concatenated, with a `\\key` change inserted whenever an
        element's key differs from the previous one. Returns `None` if no element provides right-hand code
        (asserts that either all or none do)."""
        rights = []
        last_key = self.first_key()
        none_found = False
        for piano_lilyable in self.list:
            lily = piano_lilyable.right_lily()
            if lily is None:
                none_found = True
                continue
            piano_lilyable_key = piano_lilyable.first_key()
            if piano_lilyable_key != last_key:
                last_key = piano_lilyable_key
                lily = rf"""\key {piano_lilyable_key} \major{self.separator}{lily}"""
            rights.append(lily)
        if none_found:
            assert rights == []
            return None
        assert len(rights) == len(self.list)
        separator = f"""\\bar "{self.bar_separator}"{self.separator}""" if self.bar_separator is not None else self.separator
        return separator.join(rights)

    def annotations_lily(self) -> Optional[str]:
        """The annotation lyrics for all elements, `separator`-joined. Returns `None` if no element has an
        annotation (asserts that either all or none do)."""
        annotations = [piano_lilyable.annotations_lily() for piano_lilyable in self.list]
        count = len([left for left in annotations if left is not None])
        if count == 0:
            return None
        assert count == len(self.list)
        return self.separator.join(annotations)


