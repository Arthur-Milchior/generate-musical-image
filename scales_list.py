#list of names,  number of bemol, number of sharp, intervals
import sys
scales =[
    (["Major"],0,0,   [2,2,1,2,2,2,1]),
    (["Major arpeggio"],0,0,   [(2,4),(2,3),(3,5)]),
    (["Dominant seventh arpeggio"],0,0,   [(2,4),(2,3),(2,3),2]),
    (["Minor harmonic"],3,0,[2,1,2,2,1,3,1]),
    (["Minor arpeggio"],0,0,   [(2,3),(2,4),(3,5)]),
    (["Blues"],3,0,[(2,3),2,(0,1),1,(2,3),2]),
    (["Pentatonic minor"],3,0,[(2,3),2,2,(2,3),2]),
    (["Pentatonic major"],0,0,[2,2,(2,3),2,(2,3)]),
    (["Whole tone"],0,1,[(1,2),(1,2),(1,2),(1,2),(1,2),(2,2)]),
    (["Chromatic"],0,0,[(0,1),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(1,1),(0,1),(1,1),(1,1),]),
    (["Minor natural","Aeolian mode"],3,0,[2,1,2,2,1,2,2]),
    (["Minor melodic"],3,0,[2,1,2,2,2,2,1]),
    (["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"],0,1,[2,2,2,1,2,1,2]),
    (["Altered", "Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],7,0,[1,2,1,2,2,2,2]),
    (["Augmented",],0,0,[(2,3),(0,1),(2,3),(0,1),(2,3),1]),
    (["Prometheus","Mystic chord"],1,1,[2,2,2,(2,3),1,2]),
    (["Tritone",],1,0,[1,3,(2,2),(0,1),(2,3),2]),
    (["Bebop dominant",],0,0,[2,2,1,2,2,1,(0,1),1]),
    (["Bebop dorian","Bebop minor"],1,0,[2,1,(0,1),1,2,2,1,2,]),
    (["Alternate bebop dorian"],2,0,[2,1,2,2,2,1,(0,1),1,]),
    (["Bebop major",],0,0,[2,2,1,2,(0,1),1,2,1]),
    (["Bebop melodic minor",],0,0,[2,1,2,2,(0,1),1,2,1]),
    (["Bebop harmonic minor","Bebop natural minor"],3,0,[2,1,2,2,1,2,(0,1),1]),
    (["Double harmonic major","Byzantine", "Arabic", "Gypsi major"],0,0,[1,3,1,2,1,3,1]),
    (["Enigmatic"],0,0,[1,3,2,2,2,1,1]),
    (["Descending Enigmatic"],0,0,[1,3,1,3,2,1,1]),
    (["Flamenco mode"],0,0,[1,3,1,2, 1, 3, 1]),
    (["Hungarian","Hungarian Gypsy"],3,0,[2,1,3,1,1,2,2]),
    (["Half diminished"],5,0,[2,1,2,1,2,2,2]),
    (["Harmonic major"],0,0,[2,2,1,2,1,3,1]),
    (["Hirajōshi Burrows"],0,1,[(2,4),2,1,(2,4),1]),
    (["Hirajōshi Sachs-Slonimsky"],0,0,[1,(2,4),1,(2,4),2]),
    (["Hirajōshi Kostka and Payne-Speed"],0,0,[2,1,(2,4),1,(2,4)]),
    (["Hungarian minor"],3,1,[2,1,3,1,1,3,1]),
    (["Greek Dorian tonos (diatonic genus)","Phrygian mode"],3,0,[1,2,2,2,1,2,2]),
    (["Miyako-bushi"],2,0,[1,(2,4),2,1,(2,4)]),
    (["Insen"],4,0,[1,(2,4),2,(2,3),2]),
    (["Iwato"],5,0,[1,(2,4),1,(2,4),2]),
    (["Lydian augmented"],0,3,[2,2,2,2,1,2,1]),
    (["Major Locrian"],5,0,[2,2,1,1,2,2,2]),
    (["Minyo"],0,0,[(2,3),2,(2,3),2,2]),
    (["Neapolitan minor"],4,0,[1,2,2,2,1,3,1]),
    (["Neapolitan major"],0,0,[1,2,2,2,2,2,1]),
    (["Pelog"],4,0,[1,2,3,1,1,2, 2,]),
    (["Pelog bem"],4,0,[1,(2,5),1,1,(2,4)]),
    (["Pelog barang"],4,0,[2,(2,4),1,2,(2,3)]),
    (["Persian"],5,0,[1,3,1,1,2,3,1]),
    (["Phrygian dominant"],4,0,[1,3,1,2,1,2,2]),
    (["Greek Phrygian tonos (diatonic genus)"],0,0,[2,1,2,2,2,1,2]),
    (["Greek Phrygian tonos (chromatic genus)"],0,0,[3,1,1, 2 ,3,1,1]),
    (["Slendro"],0,0,[2,(2,3),2,2,(2,3)]),
    (["Two-semitone tritone"],0,0,[1,(0,1),(2,4),1,1,(2,4)]),
    (["Ukrainian Dorian"],2,1,[2,1,3,1,2,1,2]),
    (["Misheberak"],0,0,[2,1,3,1,2,1,2]),
    (["Yo ascending"],2,0,[2,(2,3),2,(2,3),2]),
    (["Yo descending"],2,0,[2,(2,3),2,2,(2,3)]),
    (["Yo with auxiliary"],2,0,[2,1,2,2,2,1,2]),
    (["Dorian"],2,0,[2,1,2,2,2,1,2]),
    (["Greek Dorian tonos (chromatic genus)"],0,0,[1,1,3,2,1,1,3]),
    (["Locrian"],5,0,[1,2,2,1,2,2,2]),
    (["Lydian"],0,1,[2,2,2,1,2,2,1]),
    (["Greek Lydian tonos (diatonic genus)"],0,0,[2,2,1,2,2,2,1]),
    (["Greek Lydian tonos (chromatic genus)"],0,0,[1,3,1,1,3,2,1]),
    (["Mixolydian","Adonal malakh mode"],1,0,[2,2,1,2,2,1,2]),
    (["Greek Mixolydian tonos (diatonic genus)"],0,0,[1,2,2,1,2,2,2]),
    (["Greek Mixolydian tonos (chromatic genus)"],0,0,[2,1,3,1,1,3,1]),
]
scales_correct=[]
for (names,bemol,sharp,intervals) in scales:
    diatonicSum=0
    chromaticSum=0
    intervals_correct=[]
    for interval in intervals:
        diatonic,chromatic = (1,interval) if  isinstance(interval,int) else interval
        diatonicSum+=diatonic
        chromaticSum+=chromatic
        intervals_correct.append((diatonic,chromatic))
    if diatonicSum!=7:
        print("Warning: scale %s has a diatonic sum of %d"%(names[0],diatonicSum), file=sys.stderr)
    elif chromaticSum!=12:
        print("Warning: scale %s has a chromatic sum of %d"%(names[0],chromaticSum), file=sys.stderr)
    else:
        scales_correct.append((names,bemol,sharp,intervals_correct))

scales=scales_correct
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
