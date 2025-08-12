from saxophone.fingering import main_column 
from saxophone.buttons import *
from saxophone.fingering.fingering import *
from saxophone.fingering import k


a_sharp4_tk = k.a_sharp4_k.silent_button(jay_4, g, FINGERING_TK)

b4_t = main_column.b4.silent_button(jay_k2, FINGERING_T)
c5_tk = main_column.c5.silent_button(jay_k2, FINGERING_TK)

c6_tk = main_column.c6.silent_button(jay_k2, FINGERING_TK)

a_sharp5_tk = a_sharp4_tk.add_octave()
b5_t = b4_t.add_octave()

a_sharp6_tk = k.a_sharp6_k.silent_button(f, g, FINGERING_TK)