"""Contains a class to represent a scale. 

Also contains all scales from wikipedia, which can be done using the 12 notes from chromatic scales."""

from solfege.interval import ChromaticInterval, DiatonicInterval, SolfegeInterval
import sys
from .util import Solfege_Pattern

class Scale_Pattern(Solfege_Pattern):
    def __init__(self,names,intervals,bemols=0,sharps=0):
        super().__init__(names)
        diatonicSum=0
        chromaticSum=0
        intervals_correct=[]
        for interval in intervals:
            if isinstance(interval,tuple):
                diatonic,chromatic = interval
            elif isinstance(interval,int):
                diatonic=1
                chromatic=interval
            if isinstance(diatonic,int):
                diatonic = DiatonicInterval(diatonic)
            if isinstance(chromatic,int):
                chromatic = ChromaticInterval(chromatic)
            diatonicSum+=diatonic.getNumber()
            chromaticSum+=chromatic.getNumber()
            interval= SolfegeInterval(chromatic=chromaticSum,diatonic=diatonicSum)
            intervals_correct.append(interval)
        if diatonicSum!=7:
            print("Warning: scale %s has a diatonic sum of %d"%(names[0],diatonicSum), file=sys.stderr)
        elif chromaticSum!=12:
            print("Warning: scale %s has a chromatic sum of %d"%(names[0],chromaticSum), file=sys.stderr)
        self.intervals=intervals_correct
        self.bemols=bemols
        self.sharps=sharps
        

    def getBemol(self):
        return self.bemols
    def getSharp(self):
        return self.sharps
    def getIntervals(self):
        return self.intervals
    def getChromaticIntervals(self):
        return [chromatic for (_,chromatic) in self.intervals]
    def getDiatonicInterval(self):
        return [diatonic for (diatonic,_) in self.intervals]
Solfege_Pattern.dic[Scale_Pattern]=dict()
Solfege_Pattern.set_[Scale_Pattern]=list()


Scale_Pattern(["Greek Dorian tonos (chromatic genus)"],[1,1,3,2,1,1,3],0,0),
Scale_Pattern(["Major"],   [2,2,1,2,2,2,1],0,0),
Scale_Pattern(["Major arpeggio"],   [(2,4),(2,3),(3,5)],0,0),
Scale_Pattern(["Dominant seventh arpeggio"],   [(2,4),(2,3),(2,3),2],0,0),
Scale_Pattern(["Minor harmonic"],[2,1,2,2,1,3,1],3,0),
Scale_Pattern(["Minor arpeggio"],   [(2,3),(2,4),(3,5)],0,0),
Scale_Pattern(["Blues"],[(2,3),2,(0,1),1,(2,3),2],3,0),
Scale_Pattern(["Pentatonic minor"],[(2,3),2,2,(2,3),2],3,0),
Scale_Pattern(["Pentatonic major"],[2,2,(2,3),2,(2,3)],0,0),
Scale_Pattern(["Whole tone"],[(1,2),(1,2),(1,2),(1,2),(1,2),(2,2)],0,1),
Scale_Pattern(["Chromatic"],[(0,1),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(1,1),(0,1),(1,1),(1,1),],0,0),
Scale_Pattern(["Minor natural","Aeolian mode"],[2,1,2,2,1,2,2],3,0),
Scale_Pattern(["Minor melodic"],[2,1,2,2,2,2,1],3,0),
Scale_Pattern(["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"],[2,2,2,1,2,1,2],0,1),
Scale_Pattern(["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],[1,2,1,2,2,2,2],7,0),
Scale_Pattern(["Augmented",],[(2,3),(0,1),(2,3),(0,1),(2,3),1],0,0),
Scale_Pattern(["Prometheus","Mystic chord"],[2,2,2,(2,3),1,2],1,1),
Scale_Pattern(["Tritone",],[1,3,(2,2),(0,1),(2,3),2],1,0),
Scale_Pattern(["Bebop dominant",],[2,2,1,2,2,1,(0,1),1],0,0),
Scale_Pattern(["Bebop dorian","Bebop minor"],[2,1,(0,1),1,2,2,1,2,],1,0),
Scale_Pattern(["Alternate bebop dorian"],[2,1,2,2,2,1,(0,1),1,],2,0),
Scale_Pattern(["Bebop major",],[2,2,1,2,(0,1),1,2,1],0,0),
Scale_Pattern(["Bebop melodic minor",],[2,1,2,2,(0,1),1,2,1],0,0),
Scale_Pattern(["Bebop harmonic minor","Bebop natural minor"],[2,1,2,2,1,2,(0,1),1],3,0),
Scale_Pattern(["Double harmonic major","Byzantine", "Arabic", "Gypsi major"],[1,3,1,2,1,3,1],0,0),
Scale_Pattern(["Enigmatic"],[1,3,2,2,2,1,1],0,0),
Scale_Pattern(["Descending Enigmatic"],[1,3,1,3,2,1,1],0,0),
Scale_Pattern(["Flamenco mode"],[1,3,1,2, 1, 3, 1],0,0),
Scale_Pattern(["Hungarian","Hungarian Gypsy"],[2,1,3,1,1,2,2],3,0),
Scale_Pattern(["Half diminished"],[2,1,2,1,2,2,2],5,0),
Scale_Pattern(["Harmonic major"],[2,2,1,2,1,3,1],0,0),
Scale_Pattern(["Hirajōshi Burrows"],[(2,4),2,1,(2,4),1],0,1),
Scale_Pattern(["Hirajōshi Sachs-Slonimsky"],[1,(2,4),1,(2,4),2],0,0),
Scale_Pattern(["Hirajōshi Kostka and Payne-Speed"],[2,1,(2,4),1,(2,4)],0,0),
Scale_Pattern(["Hungarian minor"],[2,1,3,1,1,3,1],3,1),
Scale_Pattern(["Greek Dorian tonos (diatonic genus)","Phrygian mode"],[1,2,2,2,1,2,2],3,0),
Scale_Pattern(["Miyako-bushi"],[1,(2,4),2,1,(2,4)],2,0),
Scale_Pattern(["Insen"],[1,(2,4),2,(2,3),2],4,0),
Scale_Pattern(["Iwato"],[1,(2,4),1,(2,4),2],5,0),
Scale_Pattern(["Lydian augmented"],[2,2,2,2,1,2,1],0,3),
Scale_Pattern(["Major Locrian"],[2,2,1,1,2,2,2],5,0),
Scale_Pattern(["Minyo"],[(2,3),2,(2,3),2,2],0,0),
Scale_Pattern(["Neapolitan minor"],[1,2,2,2,1,3,1],4,0),
Scale_Pattern(["Neapolitan major"],[1,2,2,2,2,2,1],0,0),
Scale_Pattern(["Pelog"],[1,2,3,1,1,2, 2,],4,0),
Scale_Pattern(["Pelog bem"],[1,(2,5),1,1,(2,4)],4,0),
Scale_Pattern(["Pelog barang"],[2,(2,4),1,2,(2,3)],4,0),
Scale_Pattern(["Persian"],[1,3,1,1,2,3,1],5,0),
Scale_Pattern(["Phrygian dominant"],[1,3,1,2,1,2,2],4,0),
Scale_Pattern(["Greek Phrygian tonos (diatonic genus)"],[2,1,2,2,2,1,2],0,0),
Scale_Pattern(["Greek Phrygian tonos (chromatic genus)"],[3,1,1, 2 ,3,1,1],0,0),
Scale_Pattern(["Slendro"],[2,(2,3),2,2,(2,3)],0,0),
Scale_Pattern(["Two-semitone tritone"],[1,(0,1),(2,4),1,1,(2,4)],0,0),
Scale_Pattern(["Ukrainian Dorian"],[2,1,3,1,2,1,2],2,1),
Scale_Pattern(["Misheberak"],[2,1,3,1,2,1,2],0,0),
Scale_Pattern(["Yo ascending"],[2,(2,3),2,(2,3),2],2,0),
Scale_Pattern(["Yo descending"],[2,(2,3),2,2,(2,3)],2,0),
Scale_Pattern(["Yo with auxiliary"],[2,1,2,2,2,1,2],2,0),
Scale_Pattern(["Dorian"],[2,1,2,2,2,1,2],2,0),
Scale_Pattern(["Locrian"],[1,2,2,1,2,2,2],5,0),
Scale_Pattern(["Lydian"],[2,2,2,1,2,2,1],0,1),
Scale_Pattern(["Greek Lydian tonos (diatonic genus)"],[2,2,1,2,2,2,1],0,0),
Scale_Pattern(["Greek Lydian tonos (chromatic genus)"],[1,3,1,1,3,2,1],0,0),
Scale_Pattern(["Mixolydian","Adonal malakh mode"],[2,2,1,2,2,1,2],1,0),
Scale_Pattern(["Greek Mixolydian tonos (diatonic genus)"],[1,2,2,1,2,2,2],0,0),
Scale_Pattern(["Greek Mixolydian tonos (chromatic genus)"],[2,1,3,1,1,3,1],0,0),
Scale_Pattern(["Octave"],[(7,12)],0,0),

# Ignored=[
#     "Bohlen-Pierce",
#     "alpha",
#     "Beta",
#     "Delta",
#     "Gamma",
#     "Istrian",
#      "Pfluke",
#     "Non-Pythagorean",
# ]
    # (["Algerian"],
    #  [2,1,3,1,1,3,1,1, 2,1,2,2,1,3,1,1]),
    #(["Greek Dorian tonos (enharmonic genus)"],[0,1,4,2,0,1,4]),
    #(["Greek Lydian tonos (enharmonic genus)"],[1,]),
    #(["Medieval Lydian mode"],[2,2,2,1,0,2,2,1]),
    #(["Greek Mixolydian tonos (enharmonic genus)"],[1,0,1,4,]),
    #(["Vietnamese scale of harmonics"],[3,0,1,1,2,5]),
    #(["Octatonic"],[2,1,2,1,2,1,2,1]),
    #(["Greek Phrygian tonos (enharmonic genus)"],[4,1,0, 2, 4,1,0]),
    #(["Medieval Phrygian mode"],[2,2,2,1,0,1,2,2]),
    #(["Hypophrygian mode"],[2,2,1,2,0,1,2]),
    #(["Harmonic"],0,0,[3,1,1,2,2,3]),
