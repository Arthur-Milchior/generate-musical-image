This folder contains everything which is related to musical theory.

## Files
scales.py: contains a class to represent scales pattern. This class contains the list of scales pattern, and a dictionary from name to scales.
It also contains a method to generate a concrete list of note from a scale pattern and a tonic.

chords.py: contains a class to represent chord pattern, and a list of chords.
It also contains a method to generate a concrete list of note from a chord pattern and a tonic.

interval/: contains class used to represent interval.
--A diatonic interval is an interval, counting only notes in the scale
--A chromatic interval is an interval, counting each half-tone
--Alternation is a chromatic interval used to represents sharps and bemol
--Solfege interval is a pair with a diatonic interval and a chromatic interval. Or equivalently, a diatonic interval and an alteration. This is what allows to distinguish between G and G# (same diatonic interval) and G# and Ab (same chromatic interval) 

note/: contain classes to represents notes.
--DiatonicNote represents a note as its index in the scale.
--ChromaticNote represents a note as its index in the chromatic scale.
--Note represents a note using its diatonic and chromatic position


## Dependencies

Key can depends on Note which can depend on interval.
If other import is needed, do it inside function body.