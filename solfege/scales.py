"""Contains a class to represent a scale. 

Also contains all scales from wikipedia, which can be done using the 12 notes from chromatic scales."""

from solfege.interval import ChromaticInterval, DiatonicInterval
import sys

class Scale:
    dic = dict()
    scales = set()
    def __init__(self,names,intervals,bemols=0,sharps=0):
        self.names=names
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
            interval= SolfegeInterval(chromatic=chromatic,diatonic=diatonic)
            intervals_correct.append(interval)
        if diatonicSum!=7:
            print("Warning: scale %s has a diatonic sum of %d"%(names[0],diatonicSum), file=sys.stderr)
        elif chromaticSum!=12:
            print("Warning: scale %s has a chromatic sum of %d"%(names[0],chromaticSum), file=sys.stderr)
        Scale.scales.add(self)
        for name in names:
            Scale.dic[name]=self
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
    def getNames(self):
        return self.names
    def getFirstName(self):
        return self.names[0]

Scale(["Major"],   [2,2,1,2,2,2,1],0,0),
Scale(["Major arpeggio"],   [(2,4),(2,3),(3,5)],0,0),
Scale(["Dominant seventh arpeggio"],   [(2,4),(2,3),(2,3),2],0,0),
Scale(["Minor harmonic"],[2,1,2,2,1,3,1],3,0),
Scale(["Minor arpeggio"],   [(2,3),(2,4),(3,5)],0,0),
Scale(["Blues"],[(2,3),2,(0,1),1,(2,3),2],3,0),
Scale(["Pentatonic minor"],[(2,3),2,2,(2,3),2],3,0),
Scale(["Pentatonic major"],[2,2,(2,3),2,(2,3)],0,0),
Scale(["Whole tone"],[(1,2),(1,2),(1,2),(1,2),(1,2),(2,2)],0,1),
Scale(["Chromatic"],[(0,1),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(1,1),(0,1),(1,1),(1,1),],0,0),
Scale(["Minor natural","Aeolian mode"],[2,1,2,2,1,2,2],3,0),
Scale(["Minor melodic"],[2,1,2,2,2,2,1],3,0),
Scale(["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"],[2,2,2,1,2,1,2],0,1),
Scale(["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],[1,2,1,2,2,2,2],7,0),
Scale(["Augmented",],[(2,3),(0,1),(2,3),(0,1),(2,3),1],0,0),
Scale(["Prometheus","Mystic chord"],[2,2,2,(2,3),1,2],1,1),
Scale(["Tritone",],[1,3,(2,2),(0,1),(2,3),2],1,0),
Scale(["Bebop dominant",],[2,2,1,2,2,1,(0,1),1],0,0),
Scale(["Bebop dorian","Bebop minor"],[2,1,(0,1),1,2,2,1,2,],1,0),
Scale(["Alternate bebop dorian"],[2,1,2,2,2,1,(0,1),1,],2,0),
Scale(["Bebop major",],[2,2,1,2,(0,1),1,2,1],0,0),
Scale(["Bebop melodic minor",],[2,1,2,2,(0,1),1,2,1],0,0),
Scale(["Bebop harmonic minor","Bebop natural minor"],[2,1,2,2,1,2,(0,1),1],3,0),
Scale(["Double harmonic major","Byzantine", "Arabic", "Gypsi major"],[1,3,1,2,1,3,1],0,0),
Scale(["Enigmatic"],[1,3,2,2,2,1,1],0,0),
Scale(["Descending Enigmatic"],[1,3,1,3,2,1,1],0,0),
Scale(["Flamenco mode"],[1,3,1,2, 1, 3, 1],0,0),
Scale(["Hungarian","Hungarian Gypsy"],[2,1,3,1,1,2,2],3,0),
Scale(["Half diminished"],[2,1,2,1,2,2,2],5,0),
Scale(["Harmonic major"],[2,2,1,2,1,3,1],0,0),
Scale(["Hirajōshi Burrows"],[(2,4),2,1,(2,4),1],0,1),
Scale(["Hirajōshi Sachs-Slonimsky"],[1,(2,4),1,(2,4),2],0,0),
Scale(["Hirajōshi Kostka and Payne-Speed"],[2,1,(2,4),1,(2,4)],0,0),
Scale(["Hungarian minor"],[2,1,3,1,1,3,1],3,1),
Scale(["Greek Dorian tonos (diatonic genus)","Phrygian mode"],[1,2,2,2,1,2,2],3,0),
Scale(["Miyako-bushi"],[1,(2,4),2,1,(2,4)],2,0),
Scale(["Insen"],[1,(2,4),2,(2,3),2],4,0),
Scale(["Iwato"],[1,(2,4),1,(2,4),2],5,0),
Scale(["Lydian augmented"],[2,2,2,2,1,2,1],0,3),
Scale(["Major Locrian"],[2,2,1,1,2,2,2],5,0),
Scale(["Minyo"],[(2,3),2,(2,3),2,2],0,0),
Scale(["Neapolitan minor"],[1,2,2,2,1,3,1],4,0),
Scale(["Neapolitan major"],[1,2,2,2,2,2,1],0,0),
Scale(["Pelog"],[1,2,3,1,1,2, 2,],4,0),
Scale(["Pelog bem"],[1,(2,5),1,1,(2,4)],4,0),
Scale(["Pelog barang"],[2,(2,4),1,2,(2,3)],4,0),
Scale(["Persian"],[1,3,1,1,2,3,1],5,0),
Scale(["Phrygian dominant"],[1,3,1,2,1,2,2],4,0),
Scale(["Greek Phrygian tonos (diatonic genus)"],[2,1,2,2,2,1,2],0,0),
Scale(["Greek Phrygian tonos (chromatic genus)"],[3,1,1, 2 ,3,1,1],0,0),
Scale(["Slendro"],[2,(2,3),2,2,(2,3)],0,0),
Scale(["Two-semitone tritone"],[1,(0,1),(2,4),1,1,(2,4)],0,0),
Scale(["Ukrainian Dorian"],[2,1,3,1,2,1,2],2,1),
Scale(["Misheberak"],[2,1,3,1,2,1,2],0,0),
Scale(["Yo ascending"],[2,(2,3),2,(2,3),2],2,0),
Scale(["Yo descending"],[2,(2,3),2,2,(2,3)],2,0),
Scale(["Yo with auxiliary"],[2,1,2,2,2,1,2],2,0),
Scale(["Dorian"],[2,1,2,2,2,1,2],2,0),
Scale(["Greek Dorian tonos (chromatic genus)"],[1,1,3,2,1,1,3],0,0),
Scale(["Locrian"],[1,2,2,1,2,2,2],5,0),
Scale(["Lydian"],[2,2,2,1,2,2,1],0,1),
Scale(["Greek Lydian tonos (diatonic genus)"],[2,2,1,2,2,2,1],0,0),
Scale(["Greek Lydian tonos (chromatic genus)"],[1,3,1,1,3,2,1],0,0),
Scale(["Mixolydian","Adonal malakh mode"],[2,2,1,2,2,1,2],1,0),
Scale(["Greek Mixolydian tonos (diatonic genus)"],[1,2,2,1,2,2,2],0,0),
Scale(["Greek Mixolydian tonos (chromatic genus)"],[2,1,3,1,1,3,1],0,0),
Scale(["Octave"],[(7,12)],0,0),

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
