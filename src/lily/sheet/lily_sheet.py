
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
from typing import Callable, Dict, List, Optional

from lily.lily_svg_utils import clean_svg, display_svg_file
from sh import shell
from utils.data_class_with_default_argument import DataClassWithDefaultArgument
from utils.util import assert_string_equal, save_file
from consts import generate_root_folder
from utils.util import assert_typing, ensure_folder


@dataclass(frozen=True)
class LilySheet(ABC, DataClassWithDefaultArgument):
    version: str
    time: Optional[tuple[int, int]]

    def maybe_generate(self):
        """Generate the svg, return the name of the svg without folder."""
        if self.save_file():
            self.compile()
        else:
            pass
        return self.output_file_name()
        
    def save_file(self):
        """{self.lily_code()} is saved in {self.file_prefix()}.ly. Returns whether this is a change compared to before."""
        lily_path = self.lily_path()
        code = self.lily_code()
        if os.path.isfile(lily_path):
            with open(lily_path, "r") as file:
                old_code = file.read()
                same_codes = old_code == code
                assert_string_equal(old_code, code)
                svg_exists = os.path.isfile(self.output_path())
                if same_codes and svg_exists :
                    # old code exists and svg is present. It's probably the same svg. 
                    return False
        save_file(lily_path, code)
        return True

    def compile(self):
        """Compile the lily file (assumed to exists) to svg."""
        shell(f"""lilypond -dpreview -dbackend=svg -o "{self.prefix_path()}"  "{self.lily_path()}" """)
        clean_svg(self.preview_path(), self.preview_path(), "white")
        self.remove_preview_from_filename()
        
    def remove_preview_from_filename(self):
        shell(f"""mv -f "{self.preview_path()}" "{self.output_path()}" """)

    def preview_path(self):
        """The path of the file generated with dpreview."""
        return f"{self.folder_path()}/{self.preview_file_name()}"
    
    def preview_file_name(self):
        """The path of the file generated with dpreview."""
        return f"{self.file_prefix()}.preview.svg"
    
    def output_file_name(self):
        """The path of the file generated with dpreview."""
        return f"{self.file_prefix()}.svg"

    def output_path(self):
        """The path of the file generated with dpreview."""
        return f"{self.folder_path()}/{self.output_file_name()}"

    # def compile_wav(self):
    #     """Compiles file_prefix into wav. Assumes the midi exists."""
    #     shell(f"""timidity "{self.file_prefix()}.midi" --output-mode=w -o "{self.file_prefix()}.wav" """)

    def lily_path(self):
        return f"{self.folder_path()}/{self.lily_file_name()}"
    
    def lily_file_name(self):
        return f"{self.file_prefix()}.ly"
    
    def show(self):
        """Show the output (assuming it's generated)"""
        display_svg_file(self.output_path())
    
    def folder_path(self):
        folder_path = f"{generate_root_folder}/lily"
        ensure_folder(folder_path)
        return folder_path
    
    def prefix_path(self):
        return f"{self.folder_path()}/{self.file_prefix()}"
    
    def lily_code(self):
        return f"""\\version "{self.version}"
{self._lily_code()}"""

    # Must be implemented by subclasses.

    @abstractmethod
    def file_prefix(self) -> str: ...
    """Return the file name, without any extension."""

    @abstractmethod
    def _lily_code(self) -> str: ...
    """Return the lily code."""

    # Pragma mark - DataClassWithDefaultArgument
    @classmethod
    def _default_arguments_for_constructor(cls, args, kwargs):
        kwargs = super()._default_arguments_for_constructor(args, kwargs)
        kwargs["version"] = "2.24.3"
        kwargs["time"] = None
        return kwargs
    
    @classmethod
    def _clean_arguments_for_constructor(cls, args: List, kwargs: Dict):
        args, kwargs = super()._clean_arguments_for_constructor(args, kwargs)
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "version")
        args, kwargs = cls._maybe_arg_to_kwargs(args, kwargs, "time")
        return args, kwargs

    def __post_init__(self):
        super().__post_init__()