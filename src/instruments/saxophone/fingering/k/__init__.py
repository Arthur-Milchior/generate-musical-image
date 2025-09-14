from instruments.saxophone.fingering import main_column 
from instruments.saxophone.fingering.fingering import *
from instruments.saxophone.buttons import *


f_sharp4_k = main_column.f4.add_semi_tone(jay_k1, FingeringSymbol.K_COMPLETELY_EXPOSED)
a_sharp4_k = main_column.a4.add_semi_tone(jay_k2, FingeringSymbol.K_COMPLETELY_EXPOSED)
c5_k = main_column.b4.add_semi_tone(jay_k3, FingeringSymbol.K_COMPLETELY_EXPOSED)
c5_tb = main_column.b_flat4_b.add_tone(jay_k3, jay_k2, FingeringSymbol.TB)



f_sharp5_k = f_sharp4_k.add_octave()
a_sharp5_k = a_sharp4_k.add_octave()
c6_k = c5_k.add_octave()
c6_tb = c5_tb.add_octave()

f_sharp6_k = Fingering.make("F#6", {f, jay_k2, g, a, b, octave}, FingeringSymbol.K_COMPLETELY_EXPOSED)
g6_v = Fingering.make("G6", {octave, jay_k1, f, g, b}, FingeringSymbol.V)

a_sharp6_k = Fingering.make("a#6", {octave, jay_k2, jay_k3}, FingeringSymbol.K_COMPLETELY_EXPOSED)

a6_k = a_sharp6_k.remove_semi_tone(g, a, FingeringSymbol.K_PARTIALLY_EXPOSED)

g_sharp6_dk = a6_k.remove_semi_tone(e, FingeringSymbol.DK)
g_sharp6_k = Fingering.make("g#6", {octave, b, g, f, jay_k3, jay_k2}, FingeringSymbol.K_COMPLETELY_EXPOSED)
g_sharp6_a = Fingering.make("g#6", {octave, b, g, d, jay_k3, jay_k2}, FingeringSymbol.A)

