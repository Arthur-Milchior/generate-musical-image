names_pos = [
    "E",
    "F",
    "F#",
    "G",
    "G#-Ab",
    "A",
    "Bb",
    "B",
    "C",
    "C#",
    "D",
    "Eb"]
nameFromHt = ["Unison", "Half-tone", "Tone", "Third minor", "Third major","Fourth",
              "Tritone", "Fifth", "Sixth minor", "Sixth major", "Seventh minor", "Seventh major" ]
class Interval:
    def __init__(self,ivl):
        self.ivl = ivl

    def name(self):
        octave = int(self.ivl/12)
        ivlInOctave =  (self.ivl %12)
        ivlName =  nameFromHt[ivlInOctave]
        name = ivlName + ((" and %d octave"% octave )if octave>0 else "")
        return name

