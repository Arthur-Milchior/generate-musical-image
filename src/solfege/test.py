from .note import Note, DiatonicNote, ChromaticNote
from .interval import SolfegeInterval, DiatonicInterval, ChromaticInterval
from .util import Solfege_Pattern
from .chords import Chord_Pattern
from .scales import Scale_Pattern


unison = DiatonicInterval(0)
tone = DiatonicInterval(1)
third = DiatonicInterval(2)
octave = DiatonicInterval(7)
thirdDescending = DiatonicInterval(-2)

C = DiatonicNote(0)
D = DiatonicNote(1)
E = DiatonicNote(2)
A = DiatonicNote(-2)

assert (unison+unison == unison)
assert (unison+tone == tone)
assert (tone+tone == third)
assert (third - tone == tone)
assert (tone - third == -tone)
assert (unison - third == thirdDescending)


assert (C.getOctave()==0)
#assert ((C-tone).getOctave()==-1)
assert (D.getOctave()==0)

assert (C + unison == C)
assert (C + tone == D)
assert (C + third == E)
assert (E - third == C)


unison = ChromaticInterval(0)
tone = ChromaticInterval(2)
third = ChromaticInterval(4)
octave = ChromaticInterval(12)
thirdDescending = DiatonicInterval(-4)

C = ChromaticNote(0)
D = ChromaticNote(2)
E = ChromaticNote(4)
A = ChromaticNote(-3)

assert (unison+unison == unison)
assert (unison+tone == tone)
assert (tone+tone == third)
assert (third - tone == tone)
assert (tone - third == -tone)

assert (C + unison == C)
assert (C + tone == D)
assert (C + third == E)
assert (E - third == C)


C = Note(0,0)
D = Note(2,1)
E = Note(4,2)
A = Note(-3,-2)

unison = SolfegeInterval(0,0)
diatonicSemitone = SolfegeInterval(1,0)
chromaticSemitone = SolfegeInterval(1,1)
tone = SolfegeInterval(2,1)
third = SolfegeInterval(4,2)
octave = SolfegeInterval(12,7)
thirdDescending = SolfegeInterval(-4,-2)

assert (tone==tone)
assert (tone!=third)
assert (tone+tone==third)
assert (C == C)
assert (C != D)
assert (C + tone == D)
assert (C + third == E)
assert (E - third == C)

assert (third - tone == tone)
assert (tone - tone == unison)
assert (tone - third == -tone)

assert (C.lily(False)=="c'")
assert ((C+diatonicSemitone).lily(False)=="cis'")
assert ((C+chromaticSemitone).lily(False)=="des'")

# # print (f"E-C {E-C}")
# # assert (E - C == third)
majorScale=Solfege_Pattern.dic[Scale_Pattern].get("Major")

assert(majorScale.getNotes(C)==[Note(0,0), Note(2,1), Note(4,2), Note(5,3), Note(7,4), Note(9,5), Note(11,6), Note(12,7)])
majorChord=Solfege_Pattern.dic[Chord_Pattern].get("Major triad")

assert(majorChord.getNotes(C)==frozenset({Note(0,0), Note(4,2), Note(7,4)}))
