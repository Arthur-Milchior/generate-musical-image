from instruments.saxophone.buttons import *
from instruments.saxophone.fingering.saxophone_fingering import *

"""Saxophone fingering with overtone button"""

g6_t = SaxophoneFingering.make("g6", {octave, overtone, b}, fingering_symbol=FingeringSymbol.T)
g_flat6_t = g6_t.remove_semi_tone(b_flat, FingeringSymbol.T)
f6_a = g6_t.remove_tone(a, FingeringSymbol.A)
g_flat6_v = g6_t.remove_semi_tone(jay_k2, a, FingeringSymbol.V)
e6_A = f6_a.remove_semi_tone(g, FingeringSymbol.A)
e_flat6_d = e6_A.remove_semi_tone(f, FingeringSymbol.D)

b6_v = SaxophoneFingering.make("b6", {overtone, octave, b, a, g, f, e, d}, FingeringSymbol.V)

d7_n = SaxophoneFingering.make("d7", {overtone, b})
d_flat7_c = d7_n.remove_semi_tone(f, FingeringSymbol.C)
d_sharp7_n = d_flat7_c.add_tone(a)
d_sharp7_k = d7_n.add_semi_tone(jay_k3, jay_k2, FingeringSymbol.K_COMPLETELY_EXPOSED)