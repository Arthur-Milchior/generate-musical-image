from saxophone.buttons import *
from saxophone.fingering.fingering import Fingering
from saxophone.fingering import main_column 
from saxophone.fingering.fingering import Fingering
from saxophone.fingering.fingering import *

d5_th = Fingering("d5", {jay_H2}, fingering_symbol=FINGERING_TH)
d_sharp5_t = Fingering("d#5", {jay_k4}, fingering_symbol=FINGERING_T)
d5_v = d_sharp5_t.remove_semi_tone(b, FINGERING_V)


d6_n = main_column.c_sharp6.add_semi_tone(jay_H1)

d6_t = d5_th.add_octave()
d6_v = d5_v.add_octave()

d_sharp6_t = d_sharp5_t.add_octave()
d_sharp6_n = d6_n.add_semi_tone(jay_H2)

e6_k = d_sharp6_n.add_semi_tone(jay_k4, FINGERING_K_COMPLETELY_EXPOSED)
e6_t = d6_n.add_tone(jay_H3, FINGERING_T)

f6_k = e6_k.add_semi_tone(jay_H3, FINGERING_K_COMPLETELY_EXPOSED)

### high register

a6_th = Fingering("a6", {jay_H1, b, g, octave}, FINGERING_TH)
a_sharp6_th = Fingering("a#6", {jay_H1, octave, d, e, f, g, a}, FINGERING_TH)

b6_n = Fingering("b6", {octave, jay_H1})
b6_h2_th = Fingering("b6", {octave, jay_H2, e, f,g}, FINGERING_TH)
b6_h2_tw = Fingering("b6", {octave, jay_H2, jay_k3, jay_k2}, FINGERING_TW)

c7_n = b6_n.add_semi_tone(jay_H2)

c_sharp7_k = c7_n.add_semi_tone(jay_k4, FINGERING_K_COMPLETELY_EXPOSED)
c_sharp7_t = b6_n.add_tone(jay_H3, FINGERING_T)

d7_k = c_sharp7_k.add_semi_tone(jay_H3, FINGERING_K_COMPLETELY_EXPOSED)