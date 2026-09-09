"""Fingerings introduced in Sigurd M. Rascher's "Top Tones" four-octave range book: altissimo-register
fingerings that all rely on overtones, hence always implicitly press the `octave` and `e_flat` keys (see
`RascherFingering.make`)."""
from instruments.saxophone.buttons import *
from instruments.saxophone.fingering.saxophone_fingering import *


rascher_authors = frozenset({"Rascher"})
class RascherFingering(SaxophoneFingering):
    """A `SaxophoneFingering` from Rascher's book: always attributed to `rascher_authors` and tagged
    `FingeringSymbol.RASCHER`, and always implicitly presses `octave` and `e_flat` in addition to the buttons
    given explicitly."""

    @classmethod
    def make(cls,
             chromatic_note_description: str,
            buttons: Iterator[SaxophoneButton],
            fingering_symbol: FingeringSymbol = FingeringSymbol.RASCHER,
            test:bool = False,
            authors = rascher_authors) -> Self:
        """Build a Rascher fingering for `chromatic_note_description`, pressing `buttons` plus the implicit
        `octave`/`e_flat` keys. `fingering_symbol` and `authors` accept only their default values (Rascher-only
        author/symbol) so that `add_semi_tone`/`add_octave`/etc. (which call this via `SaxophoneFingering`'s
        chaining helpers, passing through the same arguments) keep working without change."""
        assert authors == rascher_authors, f"Unexpected author {authors}"
        assert fingering_symbol == FingeringSymbol.RASCHER, f"{fingering_symbol=}"
        buttons = frozenset(buttons) | {octave, e_flat}
        return super().make(chromatic_note_description=chromatic_note_description, buttons=buttons, authors=authors, fingering_symbol=fingering_symbol, test=test)

    def _add_buttons_interval(self, interval, *args):
        """Like `SaxophoneFingering._add_buttons_interval`, but always tags the result `FingeringSymbol.RASCHER`
        (Rascher fingerings never carry another symbol)."""
        return super()._add_buttons_interval(interval, *args, FingeringSymbol.RASCHER)

f_sharp6 = RascherFingering.make("F#6", {e, f, b})

g6_ = f_sharp6.add_semi_tone(high_d)

g_sharp6 = RascherFingering.make("g#6", {e, a})
g_sharp6_ = RascherFingering.make("g#6", {e,f,b, middle_side_key})
g6 = g_sharp6.remove_semi_tone(f)

a6 = RascherFingering.make("a6", {g, a})
a_sharp6 = a6.add_semi_tone(e,f)

b6 = RascherFingering.make("b6", {f, a, b, high_d})

c7 = RascherFingering.make("c7", {e,f,b})
c7_ = b6.add_semi_tone(top_side_key)

c_sharp7 = c7.add_semi_tone(high_f)
d7 = RascherFingering.make("D7", {b, high_f})

d_sharp7 = RascherFingering.make("d#7", {e, a})
d_sharp7_ = d7.add_semi_tone(middle_side_key)

e7 = d_sharp7.add_semi_tone(g)

f7 = e7.add_semi_tone(high_d, high_e_flat)

f_sharp7 = f7.add_semi_tone(high_e)

g_sharp7 = RascherFingering.make("g#7", {e,a})
g7 = g_sharp7.remove_semi_tone(f)

a7 = RascherFingering.make("a7", {d, g,a, high_d})

a_sharp7 = a7.add_semi_tone(e, high_e_flat)

b7 = a_sharp7.add_semi_tone(high_e)

c8 = RascherFingering.make("c8", {b, e,f})
