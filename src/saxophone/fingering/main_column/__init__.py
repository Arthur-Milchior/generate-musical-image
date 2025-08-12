from saxophone.buttons import *
from saxophone.fingering.fingering import *

"""Saxophone fingering with the buttons on the main column, except for overtone.
"""

# Without octave button

c_sharp5 = Fingering("c#5", {}) # no button is pressed

c5 = c_sharp5.remove_semi_tone(a) # A touch alone

b4 = c_sharp5.remove_tone(b)
b_flat4_b = Fingering("b♭4", {b_flat}, FINGERING_B)

a4 = b4.remove_tone(a)

g4 = a4.remove_tone(g)

g_sharp4 = g4.add_semi_tone(g_sharp)
g_sharp4_2 = g4.add_semi_tone(jay_2, FINGERING_2)
g_sharp4_5 = g4.add_semi_tone(jay_5, FINGERING_5)
g_sharp4_6 = g4.add_semi_tone(jay_6, FINGERING_6)

g_flat4 = g4.remove_semi_tone(e)

f4  = g4.remove_tone(f)

e4 = f4.remove_semi_tone(e)

d4 = e4.remove_tone(d)
d_sharp4 = d4.add_semi_tone(jay_3)

c4 = d4.remove_tone(c)
c_sharp4 = c4.add_semi_tone(c_sharp)

b3 = c4.remove_semi_tone(low_b)
b_flat3 = c4.remove_tone(low_b_flat)

# with octave button.

c_sharp6 = c_sharp5.add_octave()
c6 = c5.add_octave()
b5 = b4.add_octave()
b_flat5 = b_flat4_b.add_octave()
a5 = a4.add_octave()
g5 = g4.add_octave()
g_sharp5 = g_sharp4.add_octave()
g_flat5 = g_flat4.add_octave()
f5 = f4 .add_octave()
e5 = e4.add_octave()
d5 = d4.add_octave()
d_sharp5 = d_sharp4.add_octave()




f7 = Fingering("f7", {octave, f, g, b})
e7 = Fingering("e7", {octave, e, f, a})
c7_c = Fingering("c7", {octave, f, b}, FINGERING_C)
b6_c = Fingering("b6", {octave,d, e, f, g, a, b}, FINGERING_C)
a_sharp6_v = Fingering("a#6", {octave, g}, FINGERING_V)
a6_v = a_sharp6_v.remove_semi_tone(a, FINGERING_V)
a6_tw = a_sharp6_v.remove_semi_tone(d, FINGERING_TW)
g_sharp6_n = a_sharp6_v.remove_tone(b, FINGERING_N_COMPLETLY_EXPOSED)
g6_n = g_sharp6_n.remove_semi_tone(d)
f_sharp6 = Fingering("f#6", {b, g, f}, FINGERING_N_COMPLETLY_EXPOSED)
f_sharp6_d = f_sharp6.silent_button(d, e, FINGERING_D)
f6_d = f_sharp6_d.remove_semi_tone(jay_k3, FINGERING_D)
e6_d = f6_d.remove_semi_tone(a, FINGERING_D)
