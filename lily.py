import math

lowLimit={"left":-14,"right":-3}
highLimit={"left":3,"right":14}

def defaultOctave(note,finger,restart=None):
    return 0
def actualFinger(fingering,side,chooseOctave=defaultOctave):
    text=""
    lastOctave=None
    for (note,finger) in fingering:
        octave=chooseOctave(note,finger)
        height = note.interval.diatonicInterval.di
        # if height< lowLimit[side] :
        #     octave = math.floor((height-lowLimit[side])/7)
        #     if octave<-2:
        #         octave =-2
        # elif height>highLimit[side]:
        #     octave = math.floor((height-highLimit[side])/7)+1
        #     if octave >2:
        #         octave=2
        # else:
        #     octave=0
        if octave != lastOctave:
            text+="\ottava #%d\n"%(octave)
            lastOctave=octave
        text+="""%%height:%d
%s-%d
"""%(height,note.printLily(),finger)
    return text
        
def staff(key,fingering, side):
    return """
\\new Staff{
    \\clef %s
    \\key %s \\major
%s}
"""%({"left":"bass","right":"treble"}[side],key,actualFinger(fingering,side))

def lilySide(key,fingering,side):
    return """\\version "2.18.2"
\\header{
 tagline=""
}

\\score{
%s}
"""%(staff(key,fingering,side))


def lilyBoth(key,leftFingering,rightFingering):
    return """\\version "2.18.2"
\\header{
 tagline=""
}

\\score{
  \\new PianoStaff<<
%s
%s
  >>
}"""%(staff(key,rightFingering,"right"),staff(key,leftFingering,"left"))

