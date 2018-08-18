class Penalty:
    def __init__(self,data=None,startingFinger=0, thumbTwoDiatonicNote=0, thumbTwoChromaticNote=0,endingFinger=0,nbThumbOver=0,nbWhite=0):
        self.data=data
        self.startingFinger=startingFinger
        self.thumbTwoDiatonicNote=thumbTwoDiatonicNote
        self.thumbTwoChromaticNote=thumbTwoChromaticNote
        self.endingFinger=endingFinger
        self.nbThumbOver=nbThumbOver
        self.nbWhite=nbWhite

    def __add__(self,other):
        return Penalty(data=None,startingFinger=self.startingFinger+other.startingFinger,thumbTwoDiatonicNote=self.thumbTwoDiatonicNote+other.thumbTwoDiatonicNote,thumbTwoChromaticNote=self.thumbTwoChromaticNote+other.thumbTwoChromaticNote,endingFinger=self.endingFinger+other.endingFinger,nbThumbOver=self.nbThumbOver+other.nbThumbOver,nbWhite=self.nbWhite+other.nbWhite)

    def addStartingFinger(self,finger,data=None):
        return Penalty(data or self.data,finger,self.thumbTwoDiatonicNote,self.thumbTwoChromaticNote,self.endingFinger,self.nbThumbOver,self.nbWhite)

    def addEndingFinger(self,finger,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote,self.thumbTwoChromaticNote,finger,self.nbThumbOver,self.nbWhite)

    def addThumbTwoChromaticNote(self,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote,self.thumbTwoChromaticNote+1,self.endingFinger,self.nbThumbOver,self.nbWhite)

    def addThumbTwoDiatonicNote(self,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote+1,self.thumbTwoChromaticNote,self.endingFinger,self.nbThumbOver,self.nbWhite)

    def addThumbWhite(self,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote+1,self.thumbTwoChromaticNote,self.endingFinger,self.nbThumbOver,self.nbWhite+1)

    def addPassingFinger(self,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote,self.thumbTwoChromaticNote,self.endingFinger,self.nbThumbOver+1,self.nbWhite)

    def __gt__(self,other):
        """Whether self is worse than other"""
        if self.thumbTwoDiatonicNote>other.thumbTwoDiatonicNote:
            return True
        elif self.thumbTwoDiatonicNote<other.thumbTwoDiatonicNote:
            return False
        
        elif self.nbThumbOver>other.nbThumbOver:
            return True
        elif self.nbThumbOver<other.nbThumbOver:
            return False
        
        elif self.startingFinger>other.startingFinger:
            return False
        elif self.startingFinger<other.startingFinger:
            return True
        
        if self.endingFinger>other.endingFinger:
            return True
        elif self.endingFinger<other.endingFinger:
            return False

        if self.nbWhite>other.nbWhite:
            return True
        elif self.nbWhite<other.nbWhite:
            return False
        
        if self.thumbTwoChromaticNote>other.thumbTwoChromaticNote:
            return True
        elif self.thumbTwoChromaticNote<other.thumbTwoChromaticNote:
            return False
        
        else:
            return False

        
    def warning(self):
        text=""
        if self.startingFinger<4:
            text+="Starting finger is %s.\n" % self.startingFinger
        if self.endingFinger>1:
            text+="Ending finger is %s.\n" % self.endingFinger
        if self.thumbTwoDiatonicNote:
            text+="Number of thumb passing followed by an interval of two diatonic notes: %s.\n" % self.thumbTwoDiatonicNote
        # if self.thumbTwoChromaticNote:
        #     text+="Number of other thumb passing which are followed by an interval of at least a tone and chromatic note: %s.\n" % self.thumbTwoChromaticNote
        return text

    def acceptable(self):
        return self.startingFinger in [0,4,5] and  not self.thumbTwoDiatonicNote and self.endingFinger in [0,1]
    
    # def perfect(self):
    #     return self.startingFinger in[0,4] and not self.thumbTwoChromaticNote and not self.thumbTwoDiatonicNote and self.endingFinger in [0,1]
    
    def copy(self,data=None):
        return Penalty(data or self.data,self.startingFinger,self.thumbTwoDiatonicNote,self.thumbTwoChromaticNote)
