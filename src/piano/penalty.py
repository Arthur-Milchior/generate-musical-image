from copy import *


class Penalty:
    def __init__(self, data=None, startingFinger=0, thumbNonAdjacent=0, endingFinger=0, nbThumbOver=0,
                 nbWhiteAfterThumb=0, niceExtremity=True):
        self.data = data
        self.startingFinger = startingFinger
        self.thumbNonAdjacent = thumbNonAdjacent
        self.endingFinger = endingFinger
        self.nbThumbOver = nbThumbOver
        self.nbWhiteAfterThumb = nbWhiteAfterThumb
        self.niceExtremity = niceExtremity

    def __add__(self, other):
        return Penalty(data=None, startingFinger=self.startingFinger + other.startingFinger,
                       thumbNonAdjacent=self.thumbNonAdjacent + other.thumbNonAdjacent,
                       endingFinger=self.endingFinger + other.endingFinger,
                       nbThumbOver=self.nbThumbOver + other.nbThumbOver,
                       nbWhiteAfterThumb=self.nbWhiteAfterThumb + other.nbWhiteAfterThumb,
                       niceExtremity=self.niceExtremity + other.niceExtremity)

    def addStartingFinger(self, finger, data=None):
        return Penalty(data or self.data, finger, self.thumbNonAdjacent, self.endingFinger, self.nbThumbOver,
                       self.nbWhiteAfterThumb, self.niceExtremity)

    def addEndingFinger(self, finger, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent, finger, self.nbThumbOver,
                       self.nbWhiteAfterThumb, self.niceExtremity)

    def addThumbNonAdjacent(self, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent + 1, self.endingFinger,
                       self.nbThumbOver, self.nbWhiteAfterThumb, self.niceExtremity)

    def addWhiteAfterThumb(self, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent, self.endingFinger,
                       self.nbThumbOver, self.nbWhiteAfterThumb + 1, self.niceExtremity)

    def addPassingFinger(self, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent, self.endingFinger,
                       self.nbThumbOver + 1, self.nbWhiteAfterThumb, self.niceExtremity)

    def setBadExtremity(self, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent, self.endingFinger,
                       self.nbThumbOver, self.nbWhiteAfterThumb, False)

    def setGoodExtremity(self, data=None):
        return Penalty(data or self.data, self.startingFinger, self.thumbNonAdjacent, self.endingFinger,
                       self.nbThumbOver, self.nbWhiteAfterThumb, True)

    def isBadExtremity(self):
        return not self.niceExtremity

    def isGoodExtremity(self):
        return self.niceExtremity

    def __gt__(self, other):
        """Whether self is worse than other"""
        if self.thumbNonAdjacent > other.thumbNonAdjacent:
            return True
        if self.thumbNonAdjacent < other.thumbNonAdjacent:
            return False

        if self.nbThumbOver > other.nbThumbOver:
            return True
        if self.nbThumbOver < other.nbThumbOver:
            return False

        if self.isBadExtremity() and other.isGoodExtremity():
            return True
        if other.isBadExtremity() and self.isBadExtremity():
            return Fulse

        if self.startingFinger > other.startingFinger:
            return False
        if self.startingFinger < other.startingFinger:
            return True

        if self.endingFinger > other.endingFinger:
            return True
        if self.endingFinger < other.endingFinger:
            return False

        if self.nbWhiteAfterThumb > other.nbWhiteAfterThumb:
            return True
        if self.nbWhiteAfterThumb < other.nbWhiteAfterThumb:
            return False
        return False

    def warning(self):
        text = ""
        if self.endingFinger != self.startingFinger:
            if self.startingFinger < 4:
                text += "Starting finger is %s.\n" % self.startingFinger
            if self.endingFinger > 1:
                text += "Ending finger is %s.\n" % self.endingFinger
        if self.thumbNonAdjacent:
            text += "Number of thumb passing followed by an interval which is not adjacent: %s.\n" % self.thumbNonAdjacent
        return text

    def acceptable(self):
        if self.thumbNonAdjacent:
            return False
        if self.endingFinger != self.startingFinger:
            if self.endingFinger not in [0, 1]:
                return False
            if self.startingFinger not in [0, 4, 5]:
                return False
        return True

    # def perfect(self):
    #     return self.startingFinger in[0,4] and not self.thumbTwoChromaticNote and not self.thumbTwoDiatonicNote and self.endingFinger in [0,1]

    def copy(self):
        return copy(self)
