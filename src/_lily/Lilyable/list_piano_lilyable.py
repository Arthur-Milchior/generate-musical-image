from dataclasses import dataclass
from typing import List, Optional

from _lily.Lilyable.piano_lilyable import PianoLilyable, LiteralPianoLilyable


@dataclass(eq=False)
class ListPianoLilyable(PianoLilyable):
    """Each element must have the same set of left/right/annotation"""
    list: List[PianoLilyable]
    """Separator between elements in the scale/annotation in the source code"""
    separator: str = " "
    "The bar separating part of the list"
    bar_separator: Optional[str] = None

    def first_key(self) -> str:
        return self.list[0].first_key()

    def left_lily(self) -> Optional[str]:
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
        annotations = [piano_lilyable.annotations_lily() for piano_lilyable in self.list]
        count = len([left for left in annotations if left is not None])
        if count == 0:
            return None
        assert count == len(self.list)
        return self.separator.join(annotations)


