"""Fingerings that contains buttons that are here only for the use of transition."""

from saxophone.fingering import main_column 
from saxophone.buttons import *
from saxophone.fingering.fingering import *

d4_t = main_column.d4.silent_button(jay_2, FingeringSymbol.T)
e4_t = main_column.e4.silent_button(jay_3, FingeringSymbol.T)
f4_t = main_column.f4.silent_button(jay_3, FingeringSymbol.T)
a4_t = main_column.a4.silent_button(jay_4, FingeringSymbol.T)
b_flat4_c = main_column.b_flat4_b.silent_button(e, FingeringSymbol.C)
b_flat4_i = main_column.b_flat4_b.silent_button(f, FingeringSymbol.I) 
b_flat4_tb = main_column.b_flat4_b.silent_button(jay_4, FingeringSymbol.TB)




e5_t = e4_t.add_octave()
f5_t = f4_t.add_octave()
a5_t = a4_t.add_octave()
b_flat5_c = b_flat4_c.add_octave()
b_flat5_i = b_flat4_i.add_octave()
b_flat5_tb = b_flat4_tb.add_octave()
c_sharp6_p = main_column.c_sharp6.silent_button(e, f, FingeringSymbol.P)


a_sharp6_n = main_column.a_sharp6_v.silent_button(e, f)
a6_silent_n = main_column.a6_tw.silent_button(e, f, a)
g_sharp6_d = a6_silent_n.remove_semi_tone(b, FingeringSymbol.D)