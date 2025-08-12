from typing import Dict

from saxophone.fingering import cn
from saxophone.fingering.cn import cn_silent
from saxophone.fingering import k
from saxophone.fingering.k import k_silent
from saxophone.fingering.main_column import silent
from saxophone.fingering.fingering import *
from saxophone.fingering import rascher
from saxophone.fingering.overtone import overtone

class Fingerings():
    def __init__(self, *fingerings: Fingering):
        self.fingerings = list(fingerings)
        first = fingerings[0]
        value = first.value
        for fingering in fingerings:
            assert value == fingering.value, f"""{fingering} has not same value as {first}"""
        assert value not in value_to_fingerings, f"""{value} already in {value_to_fingerings[value]}"""
        value_to_fingerings[value] = self
        for i in range (len(fingerings)):
            first = fingerings[i]
            first.added_to_some_fingerings = True
            for j in range(i+1, len(fingerings)):
                second = fingerings[j]
                assert first != second, f"""{first.get_name_with_octave()}: {first} and {second} have the same buttons"""
                if first.fingering_symbol != FINGERING_RASCHER:
                    assert first.fingering_symbol != second.fingering_symbol, f"""{first.get_name_with_octave()}: {first} and {second} have the same symbols"""

    def add_octave(self, *fingerings: Fingering):
        plus_octave = [fingering.add_octave() for fingering in self.fingerings]
        return Fingerings(*plus_octave, *fingerings)
    
    def __repr__(self):
        return f"""Fingerings({", ".join(str(fingering) for fingering in  self.fingerings)})"""
    
    def __iter__(self):
        return iter(self.fingerings)
    
    def __len__(self):
        return len(self.fingerings)
    
    def get_name_with_octave(self):
        return self.fingerings[0].get_name_with_octave()

value_to_fingerings: Dict[int, Fingerings] = dict()

b_flat_3 = Fingerings(main_column.b_flat3)

b_3 = Fingerings(main_column.b3)

c4 = Fingerings(main_column.c4)

c_sharp4 = Fingerings(main_column.c_sharp4)

d4 = Fingerings(main_column.d4, silent.d4_t)

d_sharp4 = Fingerings(main_column.d_sharp4)

e4 = Fingerings(main_column.e4, silent.e4_t)

f4 = Fingerings(main_column.f4, silent.f4_t)

f_sharp4 = Fingerings(main_column.g_flat4, k.f_sharp4_k)

g4 = Fingerings(main_column.g4)

g_sharp4 = Fingerings(main_column.g_sharp4, main_column.g_sharp4_2, main_column.g_sharp4_5, main_column.g_sharp4_6)

a4 = Fingerings(main_column.a4, silent.a4_t)

a_sharp4 = Fingerings(k.a_sharp4_k, main_column.b_flat4_b, silent.b_flat4_c, silent.b_flat4_i, k_silent.a_sharp4_tk, silent.b_flat4_tb)

b4 = Fingerings(main_column.b4, k_silent.b4_t)

c5 = Fingerings(main_column.c5, k.c5_k, k_silent.c5_tk, k.c5_tb)

c_sharp5 = Fingerings(main_column.c_sharp5)

d5 = Fingerings(main_column.d5, cn_silent.d5_tw, cn.d5_th, cn.d5_v, cn_silent.d5_vb)

d_sharp5 = Fingerings(main_column.d_sharp5, cn.d_sharp5_t, cn_silent.d_sharp5_v)

e5 = Fingerings(main_column.e5, silent.e5_t)

f5 = Fingerings(main_column.f5, silent.f5_t)

f_sharp5 = Fingerings(main_column.g_flat5, k.f_sharp5_k)

g5 = Fingerings(main_column.g5)

g_sharp5 = Fingerings(main_column.g_sharp5)

a5 = Fingerings(main_column.a5, silent.a5_t)

a_sharp5 = Fingerings(main_column.b_flat5, silent.b_flat5_c, silent.b_flat5_i, k.a_sharp5_k, k_silent.a_sharp5_tk, silent.b_flat5_tb)

b5 = Fingerings(main_column.b5, k_silent.b5_t)

c6 = Fingerings(main_column.c6,  k.c6_k, k_silent.c6_tk, k.c6_tb, cn_silent.c6_d)

c_sharp6 = Fingerings(main_column.c_sharp6, silent.c_sharp6_p)

d6 = Fingerings(cn.d6_n, cn_silent.d6_p, cn.d6_t, cn.d6_v, cn_silent.d6_vb)

d_sharp6 = Fingerings(cn.d_sharp6_n, cn_silent.d_sharp6_p, cn.d_sharp6_t, cn_silent.d_sharp6_v, overtone.e_flat6_d)

e6 = Fingerings(cn.e6_k, overtone.e6_A, cn.e6_t, main_column.e6_d)

f6 = Fingerings(cn.f6_k, overtone.f6_a, main_column.f6_d)

f_sharp6 = Fingerings(rascher.f_sharp6, main_column.f_sharp6, k.f_sharp6_k, overtone.g_flat6_t, overtone.g_flat6_v, main_column.f_sharp6_d)

g6 = Fingerings(rascher.g6, rascher.g6_, main_column.g6_n, overtone.g6_t, k.g6_v)

g_sharp6 = Fingerings(rascher.g_sharp6, rascher.g_sharp6_, main_column.g_sharp6_n, k.g_sharp6_k, k.g_sharp6_a, silent.g_sharp6_d, k.g_sharp6_dk)

a6 = Fingerings(rascher.a6, silent.a6_silent_n, k.a6_k, main_column.a6_tw, cn.a6_th, main_column.a6_v)

a_sharp6 = Fingerings(rascher.a_sharp6, silent.a_sharp6_n, k.a_sharp6_k, k_silent.a_sharp6_tk, cn.a_sharp6_th, main_column.a_sharp6_v)

b6 = Fingerings(rascher.b6, cn.b6_n, cn_silent.b6_k, main_column.b6_c, cn.b6_h2_th, cn.b6_h2_tw, overtone.b6_v)

c7 = Fingerings(rascher.c7, rascher.c7_, cn.c7_n, cn_silent.c7_k, main_column.c7_c, cn_silent.c7_t)

c_sharp7 = Fingerings(rascher.c_sharp7, cn.c_sharp7_k, overtone.d_flat7_c, cn.c_sharp7_t)

d7 = Fingerings(rascher.d7, overtone.d7_n, cn.d7_k)

d_sharp7 = Fingerings(rascher.d_sharp7, rascher.d_sharp7_, overtone.d_sharp7_n, overtone.d_sharp7_k)

e7 = Fingerings(rascher.e7, main_column.e7)

f7 = Fingerings(rascher.f7, main_column.f7)

f_sharp7 = Fingerings(rascher.f_sharp7)

g7 = Fingerings(rascher.g7)

g_sharp7 = Fingerings(rascher.g_sharp7)

a7 = Fingerings(rascher.a7)

a_sharp7 = Fingerings(rascher.a_sharp7)

b7 = Fingerings(rascher.b7)

c8 = Fingerings(rascher.c8)

for fingerings in value_to_fingering.values():
    for fingering in fingerings:
        assert fingering.added_to_some_fingerings, f"""{fingering} was not added to a Fingerings.\n {"\n".join(fingering.stack)}"""