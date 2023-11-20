


# Twelve notes around middle C (with F#=Gb twice), and the number of bemol to add for this key
twelve_notes = []
for (diatonic, alteration, nbBemol) in [(0, 0, 0),  # C
                                        (-3, 0, -1),  # G
                                        (3, 0, 1),  # F
                                        (1, 0, -2),  # D
                                        (-1, -1, 2),  # Bb
                                        (-2, 0, -3),  # A
                                        (2, -1, 3),  # Eb
                                        (2, 0, -4),  # E
                                        (-2, -1, 4),  # Ab
                                        (-1, 0, -5),  # B
                                        (1, -1, 5),  # Db
                                        (3, 1, -6),  # F#
                                        # (-3,-1,6),#Gb
                                        ]:
    note = Note(diatonic=diatonic, alteration=alteration)
    twelve_notes.append((note, nbBemol))
    # print("Diatonic %s, alteration=%s, note %s"%(diatonic,alteration,note))
#     (Note(diatonic=0,alteration=0),0),#C
#     (Note(diatonic=-3,alteration=0),-1),#G
#     (Note(diatonic=3,alteration=0),1),#F
#     (Note(diatonic=1,alteration=0),-2),#D
#     (Note(diatonic=-1,alteration=-1),2),#Bb
#     (Note(diatonic=-2,alteration=0),-3),#A
#     (Note(diatonic=2,alteration=-1),3),#Eb
#     (Note(diatonic=2,alteration=0),-4),#E
#     (Note(diatonic=-2,alteration=-1),4),#Ab
#     (Note(diatonic=-1,alteration=0),-5),#B
#     (Note(diatonic=1,alteration=-1),5),#Db
#     (Note(diatonic=3,alteration=1),-6),#F#
#     (Note(diatonic=-3,alteration=-1),6),#Gb
# C#
#
# G#

# D#

# A#

# E#

# B#
# ]

