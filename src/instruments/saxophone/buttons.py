"""Defines `SaxophoneButton` (one physical key on the saxophone) and creates the module-level instance for
every button on the horn (e.g. `jay_H1`/`londeix_C1`/`high_d`, `b_flat`, `jay_k1`/`londeix_tf`, ...). Each
button is created exactly once here via `SaxophoneButton.make()`; other modules import these names to say
which buttons a given `SaxophoneFingering` presses."""
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Self

from utils.svg.svg_line import SvgLine
from utils.util import assert_typing


@dataclass(frozen=True)
class SaxophoneButton(SvgLine):
    """One physical key/button on the saxophone, drawn as a single SVG shape that can be rendered either
    unfilled (not pressed) or filled (pressed) as part of a `SaxophoneFingering` diagram.

    Every button used anywhere in the fingering charts is created once, at import time, via `make()` (see the
    module-level instances below); creation order determines `index`, and every instance is also appended to
    the module-level `buttons` registry so a full fingering diagram can draw every button (selected or not)."""
    first_free_index: ClassVar[int] = 0
    """Running counter used by `make()` to assign each new button a unique, creation-order `index`."""

    svg_unfilled: str
    """The button's shape as a raw SVG element string (e.g. `<ellipse .../>`), with `fill:none` so it can be
    turned on/off by `svg_line()`."""

    londeix: str
    """The button's name in Londeix notation (e.g. `"C4"`, `"1"`, `"Tf"`)."""

    index: int
    """Creation-order index, assigned by `make()` from `first_free_index`; used to sort buttons deterministically."""

    name:Optional[str]=None
    """Human-readable note/key name (e.g. `"F6"`, `"B♭3"`), used in `__repr__` and in the SVG comment; `None`
    for buttons that have no associated note name (e.g. the octave key)."""

    jay_name: Optional[str]= None
    """The button's name in Jay's notation (e.g. `"H3"`, `"L1"`, `"k1"`); `None` when Jay's book has no name
    for this button."""

    @classmethod
    def make(cls,
             svg_unfilled:str,
             jay_name: Optional[str],
             londeix: str,
             name: Optional[str] = None) -> Self:
        """Create a new button, assign it the next `index`, and return it. `__post_init__` registers it in the
        module-level `buttons` list."""
        index = SaxophoneButton.first_free_index
        SaxophoneButton.first_free_index += 1
        return cls(svg_unfilled=svg_unfilled, jay_name=jay_name, londeix=londeix, name=name, index=index)

    def __post_init__(self):
        """Register this button in the module-level `buttons` list so it appears (unselected by default) in
        every rendered fingering diagram."""
        buttons.append(self)

    def __repr__(self):
        """Return the button's human-readable `name`."""
        return self.name

    def __lt__(self, other):
        """Order buttons by creation-order `index`."""
        assert isinstance(other, SaxophoneButton)
        return self.index < other.index

    def __eq__(self, other: "SaxophoneButton"):
        """Buttons are unique objects: equal only to themselves (identity), never to an equivalent copy."""
        assert_typing(other, SaxophoneButton)
        return self is other

    def __hash__(self):
        """Hash by `svg_unfilled`, which is unique per button."""
        return hash(self.svg_unfilled)

    #pragma mark - SvgLine

    def svg_line(self, selected: bool) -> str:
        """Return this button's SVG element, filled in black if `selected` (pressed) or white otherwise (not
        pressed), with a trailing SVG comment naming the button for readability of the generated file."""
        color = "000000" if selected else "ffffff"
        svg = self.svg_unfilled.replace("fill:none", f"fill:#{color}")
        return f"{svg}<!-- {self.name} -->"

# Registry of every button ever created (in creation order); `SaxophoneFingering.svg_lines` draws all of them,
# selected or not, so a diagram always shows the full instrument.
buttons: List[SaxophoneButton] = []

jay_H3 = londeix_C4 = high_f = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="56.05289" cy="17.782585" rx="3.1408629" ry="4.7741113" />""",
    "H3", "C4", "F6")
jay_H2 = londeix_C2 = high_d_sharp= high_e_flat = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="61.4697" cy="28.255554" rx="3.1408629" ry="4.7741113" />""",
    "H2", "C2", "D#6")
jay_H1 = londeix_C1 = high_d = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="51.692" cy="30.571587" rx="3.1408629" ry="4.7741113" />""",
    "H1",  "C1", "D6")

octave = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="19.633972" cy="18.258125" rx="3.1408629" ry="4.7741113" />""",
    None, "clé d'octave")

jay_A = londeix_X = overtone = SaxophoneButton.make(
    """<circle  style="fill:none;stroke:#000000;stroke-width:0.4404"  cx="32.677612"  cy="0"  r="3.6944413" />""",
    "A", "X", "overtone")#
jay_L1 = londeix_1 = b = SaxophoneButton.make(
    """<circle style="fill:none;stroke:#000000;stroke-width:0.79375" cx="32.921547" cy="11.447777" r="6.6586294" />""",
    "L1", "1", "B")
jay_B = londeix_P = b_flat = SaxophoneButton.make(
    """<circle  style="fill:none;stroke:#000000;stroke-width:0.4404"  cx="41.47079"  cy="18.843323"  r="3.6944413" />""",
    "B", "P", "B♭")#
jay_L1 = londeix_2 = a= SaxophoneButton.make(
    """<circle style="fill:none;stroke:#000000;stroke-width:0.79375" cx="34.26963" cy="30.577904" r="6.6586294" />""",
    "L2" , "2", "A")
jay_L3 = londeix_3 = g= SaxophoneButton.make(
    """<circle style="fill:none;stroke:#000000;stroke-width:0.79375" cx="34.324356" cy="47.269333" r="6.6586294" />""",
    "L3", "3", "G")


jay_4 = londeix_g_sharp = g_sharp = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="48.80817" cy="53.69032" rx="5.653553" ry="3.0152285" />""",
    "4" , "G#")
jay_2 = londeix_C_sharp = c_sharp = SaxophoneButton.make(
    """<ellipse style="fill:none;stroke:#000000;stroke-width:0.79375" cx="58.19344" cy="59.09695" rx="3.1408629" ry="4.7741113" />""",
    "2", "C#")
jay_5 = londeix_8 = low_b = SaxophoneButton.make(
    """<ellipse  style="fill:none;stroke:#000000;stroke-width:0.79375"  cx="40.05709"  cy="59.27319"  rx="3.1408629"  ry="4.7741113" />""",
    "5", "8", "B3")#
jay_6 = londeix_Bb = low_b_flat = SaxophoneButton.make(
    """<ellipse  style="fill:none;stroke:#000000;stroke-width:0.79375"  cx="49.12113"  cy="64.14896"  rx="5.653553"  ry="3.0152285" />""",
    "6", "Bb", "B♭3")#

jay_k4 = londeix_c3 = high_e = top_side_key = SaxophoneButton.make(
    """<rect  style="fill:none;stroke:#000000;stroke-width:0.79375"  width="4.2715735"  height="13.06599"  x="10"  y="59.2778" />""",
    "k4", "C3","E6")#
jay_k3 = londeix_tc = middle_side_key = SaxophoneButton.make(
    """<rect  style="fill:none;stroke:#000000;stroke-width:0.79375"  width="4.2715735"  height="13.06599"  x="10"  y="72.62829" />""",
    "k3", "Tc")#
jay_k2 = londeix_ta = SaxophoneButton.make(
    """<rect  style="fill:none;stroke:#000000;stroke-width:0.79375"  width="4.2715735"  height="13.06599"  x="10"  y="85.97878" />""",
    "k2", "Ta")#
londeix_c5 = high_f_sharp = SaxophoneButton.make(
    """<rect  style="fill:none;stroke:#000000;stroke-width:0.488711"  width="3.3760049"  height="12.477427"  x="15.748596"  y="97.76025" />""",
    None, "C5", "F#6")#
jay_k1 = londeix_tf = SaxophoneButton.make(
    """<rect  style="fill:none;stroke:#000000;stroke-width:0.58909"  width="4.3111863"  height="9.7602797"  x="19.628777"  y="111.8532" />""",
    "k1", "Tf")#


jay_R1 = londeix_4 = f = SaxophoneButton.make(
    """<circle  style="fill:none;stroke:#000000;stroke-width:0.79375"  cx="33.431458"  cy="89.54523"  r="6.6586294" />""",
    "R1", "4", "F")#
jay_R2 = londeix_5 = e = SaxophoneButton.make(
    """<circle  style="fill:none;stroke:#000000;stroke-width:0.79375"  cx="33.431458"  cy="107.16762"  r="6.6586294" />""",
    "R2", "5", "E")#
jay_R3 = londeix_6 = d = SaxophoneButton.make(
    """<circle  style="fill:none;stroke:#000000;stroke-width:0.79375"  cx="33.431458"  cy="123.85905"  r="6.6586294" />""",
    "R3", "6", "D")#
jay_3 = londeix_3 = e_flat = b_sharp = SaxophoneButton.make(
    """<rect style="fill:none;stroke:#000000;stroke-width:0.79375" width="17.840101" height="8.0406094" x="9.867577" y="131.06013" />""",
    "3", "D#")
jay_1 = londeix_7 = c = SaxophoneButton.make(
    """<rect style="fill:none;stroke:#000000;stroke-width:0.79375" width="17.840101" height="8.0406094" x="9.86734" y="140.51723" />""",
    "1", "7", "C")



