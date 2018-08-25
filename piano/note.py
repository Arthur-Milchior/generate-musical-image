import solfege.note
class Note(solfege.note.Note):
    def __init__(interval=None):
        super().__init__(interval=interval)
        
    def adjacent(self,other):
        # selfDebug=self.baseOctave()
        # otherDebug=other.baseOctave()
        # if other<= self:
        #     print("Notes %s and %s are in the wrong order"%(selfDebug,otherDebug))
        #     return other.adjacent(self)
        # distance = other.getNumber()-self.getNumber()
        # adjacent= distance==1 or (self.getNumber()+2==other.getNumber() and self.baseOctave().getNumber() not in [3,4,10,11])
        # debug("Notes %s and %s are adjacent: %s"%(selfDebug,otherDebug,adjacent))
        # return adjacent
        return abs(other.getNumber()-self.getNumber())<=2
    
    def isBlack(self):
        blacks = {1,3,6,8, 10}
        return (self.getChromaticInterval().getNumber()%12) in blacks

twelve_notes=[Note(note) for note in solfege.note.twelve_notes]
