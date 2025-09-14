from instruments.saxophone.fingering import cn
from instruments.saxophone.fingering import main_column 
from instruments.saxophone.fingering.fingering import Fingering
from instruments.saxophone.buttons import *
from instruments.saxophone.fingering.fingering import *

"""Contains fingering that add buttons that don't change the sounds, and that contains a C1, C2, C3 or C4"""

d5_tw = cn.d5_th.silent_button(c, FingeringSymbol.TW)
d5_vb = cn.d5_v.silent_button(b_flat, FingeringSymbol.VB)
d_sharp5_v = cn.d_sharp5_t.silent_button(a, FingeringSymbol.V)

c6_d = main_column.c6.silent_button(jay_H1, b, FingeringSymbol.D)

d6_p = cn.d6_n.silent_button(d,e,f, FingeringSymbol.P)

d_sharp6_p = d6_p.add_semi_tone(jay_H2, FingeringSymbol.P)
d_sharp6_v = cn.d_sharp6_t.silent_button(a, FingeringSymbol.V)
d6_vb = d5_vb.add_octave()


b6_k = cn.b6_n.silent_button(jay_k2, jay_k3, FingeringSymbol.K_COMPLETELY_EXPOSED)

c7_k = cn.c7_n.silent_button(jay_k2, jay_k3, FingeringSymbol.K_COMPLETELY_EXPOSED)
c7_t = cn.c7_n.silent_button(e, f, g, FingeringSymbol.T)

