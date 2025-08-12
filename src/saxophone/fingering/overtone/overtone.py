from saxophone.buttons import *
from saxophone.fingering.fingering import *

"""Saxophone fingering with overtone button"""

g6_t = Fingering("g6", {octave, overtone, b}, fingering_symbol=FINGERING_T)
g_flat6_t = g6_t.remove_semi_tone(b_flat, FINGERING_T)
f6_a = g6_t.remove_tone(a, FINGERING_A)
g_flat6_v = g6_t.remove_semi_tone(jay_k2, a, FINGERING_V)
e6_A = f6_a.remove_semi_tone(g, FINGERING_A)
e_flat6_d = e6_A.remove_semi_tone(f, FINGERING_D)

b6_v = Fingering("b6", {overtone, octave, b, a, g, f, e, d}, FINGERING_V)

d7_n = Fingering("d7", {overtone, b})
d_flat7_c = d7_n.remove_semi_tone(f, FINGERING_C)
d_sharp7_n = d_flat7_c.add_tone(a)
d_sharp7_k = d7_n.add_semi_tone(jay_k3, jay_k2, FINGERING_K_COMPLETELY_EXPOSED)