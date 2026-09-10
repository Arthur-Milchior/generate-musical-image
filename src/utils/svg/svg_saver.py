
from abc import ABC, abstractmethod

from utils.util import assert_typing, ensure_folder, save_file


class SvgSaver(ABC):
    """Protocol for "this object can render itself to an SVG string (`svg()`) and be saved to a file
    (`save_svg`)", with a file-naming convention (`svg_name`) shared by every subclass."""

    def svg_name(self, keep_in_collection:bool = False, **kwargs) -> str:
        """
        the name for the file
        Starts with "_" if `keep_in_collection` to ensure anki "check_media" don't delete it.
        Then _svg_name_base()
        then .svg
        """
        prefix = "_" if keep_in_collection else ""
        return f"{prefix}{self._svg_name_base(**kwargs)}.svg"
    
    def save_svg(self, folder_path: str, **kwargs) -> str:
        """Save the svg in `folder_path`. Return the file name."""
        assert_typing(folder_path, str)
        ensure_folder(folder_path)
        svg_name = self.svg_name(**kwargs)
        file_path = f"{folder_path}/{svg_name}"
        svg = self.svg(**kwargs)
        save_file(file_path, svg)
        return svg_name

    #Must be implemented by subclasses
    @abstractmethod
    def svg(self) -> str:
        """The content of the svg."""
        ...

    @abstractmethod
    def _svg_name_base(self, **kwargs) -> str:
        """The base of the name of the file, without '.svg'"""
        ...