
from solfege.pattern.chord import chord_pattern


for chord in chord_pattern:
    #This cause arpeggio to be registered
    chord.to_arpeggio_pattern()
