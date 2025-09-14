from instruments.saxophone.buttons import *
from instruments.saxophone.fingering.fingering import *

"Fingerings introduceds in Sigurd M. Raschèr four-octave range book"


rascher_authors = frozenset({"Rascher"})
class RascherFingering(Fingering):

    @classmethod
    def make(cls,
             chromatic_note_description: str,
            buttons: Iterator[SaxophoneButton],
            fingering_symbol: FingeringSymbol = FingeringSymbol.RASCHER,
            test:bool = False,
            authors = rascher_authors) -> Self:
        """The two last argument allows to use the same constructor"""
        assert authors == rascher_authors, f"Unexpected author {authors}"
        assert fingering_symbol == FingeringSymbol.RASCHER, f"{fingering_symbol=}"
        buttons = frozenset(buttons) | {octave, e_flat}
        return super().make(chromatic_note_description=chromatic_note_description, buttons=buttons, authors=authors, fingering_symbol=fingering_symbol, test=test)

    def _add_buttons_interval(self, interval, *args):
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
