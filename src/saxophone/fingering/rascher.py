from saxophone.buttons import *
from saxophone.fingering.fingering import *

"Fingerings introduceds in Sigurd M. Raschèr four-octave range book"


authors = frozenset({"Rascher"})
class RascherFingering(Fingering):
    def __init__(self, chromatic_note_description: str, buttons: Iterator[SaxophoneButton], authors: frozenset[str]=authors, fingering_symbol: str = FINGERING_RASCHER):
        """The two last argument allows to use the same constructor"""
        assert authors == authors, f"Unexpected author {authors}"
        assert fingering_symbol == FINGERING_RASCHER, f"{fingering_symbol=}"
        buttons = frozenset(buttons) | {octave, e_flat}
        super().__init__(chromatic_note_description, buttons, authors="Raschèr", fingering_symbol=FINGERING_RASCHER)

    def _add_buttons_interval(self, interval, *args):
        return super()._add_buttons_interval(interval, *args, FINGERING_RASCHER)

f_sharp6 = RascherFingering("F#6", {e, f, b})

g6_ = f_sharp6.add_semi_tone(high_d)

g_sharp6 = RascherFingering("g#6", {e, a})
g_sharp6_ = RascherFingering("g#6", {e,f,b, middle_side_key})
g6 = g_sharp6.remove_semi_tone(f)

a6 = RascherFingering("a6", {g, a})
a_sharp6 = a6.add_semi_tone(e,f)

b6 = RascherFingering("b6", {f, a, b, high_d}, FINGERING_N_COMPLETLY_EXPOSED)

c7 = RascherFingering("c7", {e,f,b})
c7_ = b6.add_semi_tone(top_side_key)

c_sharp7 = c7.add_semi_tone(high_f)
d7 = RascherFingering("D7", {b, high_f})

d_sharp7 = RascherFingering("d#7", {e, a})
d_sharp7_ = d7.add_semi_tone(middle_side_key)

e7 = d_sharp7.add_semi_tone(g)

f7 = e7.add_semi_tone(high_d, high_e_flat)

f_sharp7 = f7.add_semi_tone(high_e)

g_sharp7 = RascherFingering("g#7", {e,a})
g7 = g_sharp7.remove_semi_tone(f)

a7 = RascherFingering("a7", {d, g,a, high_d})

a_sharp7 = a7.add_semi_tone(e, high_e_flat)

b7 = a_sharp7.add_semi_tone(high_e)

c8 = RascherFingering("c8", {b, e,f})
