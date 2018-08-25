#from solfege.note import *
from solfege.interval import ChromaticInterval
from solfege.note import ChromaticNote


fret_distance = 50
string_distance = 30
circle_radius  = 11

distance_string = {
    1:ChromaticNote(-20),
    2:ChromaticNote(-15),
    3:ChromaticNote(-10),
    4:ChromaticNote(-5),
    5:ChromaticNote(-1),
    6:ChromaticNote(4),
}

class Pos:
    """A position on the guitar, that is, a string and a fret. Fret 0 is open. Fret None is not played"""
    def __init__(self, string,fret):
        self.string = string
        self.fret = fret

    def _getChromaticInterval(self):
        """The distance in half-tone between this note and the first 0th string on the first fret, that is, E """
        return distance_string[self.string]+self.fret 

    def __str__(self):
        return "(%d,%d)" %(self.string,self.fret)

    def __lt__(self, pos):
        return (pos is None or
            (self._getChromaticInterval() < pos._getChromaticInterval ()) or
            (self._getChromaticInterval() == pos._getChromaticInterval () and self.string<pos.string))
    def __eq__(self, pos):
        return self.string == pos.string and self.fret == pos.fret
    def __hash__(self):
        if self.fret is None:
            return -self.string 
        else:
            return self._getChromaticInterval()
        
    def _draw (self, f):
        """Draw this position, assuming that f already contains the svg for the fret"""
        cx = string_distance*(self.string - 0.5)
        if self.fret is None:
            f.write("""<text x="%d" y="%d" font-size="30">x</text>"""%(cx, fret_distance/3))
        elif self.fret ==0:
            f.write("""<circle cx="%d" cy="%d" r="%d" fill="white" stroke="black" stroke-width="3"/>"""%(cx, fret_distance/2, circle_radius))
        else:
            cy = (self.fret) * fret_distance
            f.write("""<circle cx="%d" cy="%d" r="%d" fill="black" />"""%(cx, cy, circle_radius))

    def __sub__(self,pos):
        """the number of semitone from self (low) to  pos"""
        return (ChromaticInterval(self._getChromaticInterval() - pos._getChromaticInterval ()))
    def add(self, i, min=0, max = 5):
        """A pos, equal to self, plus i half tone. 

        fret is minimal in [min,max]. If no such pos exists, return None"""
        if isinstance(i, chromaticinterval):
            i=i.getNumber()
        s = i +  self._getChromaticInterval()
        max_string = None
        for string in distance_string:
            if min <= s - distance_string[string] <= max:
                if (max_string is  None) or (string>max_string):
                    max_string=string
        if max_string:
            return Pos(max_string,s-distance_string[max_string])
        else:
            return None
    def toSop(self):
        """A set of pos whose only element is this position."""
        return SetOfPos({self})

    def draw(self, f, nbFretMin=3):
        """Draw a fret with this only position"""
        self.toSop().draw(f, nbFretMin=nbFretMin)
        
    def name(self):
        """The name of this position. Assuming standard guitar"""
        return names_pos[self._getChromaticInterval() %12]

class SetOfPos:
    """A set of position of the guitar"""
    def __init__(self, poss):
        self.poss = poss
        self.maxFret=0
        self.minFret=100
        m = None
        for pos in self.poss:
            if pos.fret is None:
                continue
            self.maxFret= max (self.maxFret, pos.fret)
            self.minFret= min (self.minFret, pos.fret)
            if m is None or pos < m:
                m = pos
        self.minPos= m

    def __iter__ (self):
        return iter(self.poss)
    def __lt__ (self, sop):
        """Whether each pos of this Pos belong to sop, except maybe from empty string position"""
        for pos in self.poss:
            if pos.fret is not None and pos not in sop.poss:
                return False
        return True
    def isOneMin (self):
        """Whether there is a first fret played."""
        return self.minFret ==1
    def isOpen (self):
        """Whether there is a note played free."""
        open =  (self.minFret ==0)
        if open:
            debug("is open")
            return True
        else:
            debug("not open. Minimal fret is %d" %self.minFret)
            return False

    def maxFret(self):
        return self.maxFret
    def findMinPos(self):
        return self.minPos
    
    def draw(self, f, nbFretMin = 0):
        nbFretToDraw = max(self.maxFret,nbFretMin)
        height = ((nbFretToDraw+1)*fret_distance)
        width = string_distance*6
        f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">"""%(width,height))
        for i in range (1,7):
            #columns
            x = string_distance * (i-.5)
            y1 = fret_distance/2
            y2 = fret_distance * (nbFretToDraw+.5 )
            f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />"""%(x,y1 ,x, y2))
        for i in range (1,nbFretToDraw+2):
            #lines
            x1 = string_distance/2
            x2 = string_distance * 5.5
            y =  fret_distance * (i -.5)
            f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />""" %(x1,y,x2,y))

        for pos in self.poss:
            pos._draw(f)
        f.write("</svg>")
        
    def __str__(self):
        # s = "{"
        # for pos in self.s:
        #     s += str(pos)+","
        # s+="}"
        # return s
        s ="\n"
        # pair = [pos.string,pos.fret for pos in self.s]
        for fret in range(1,self.maxFret+1):
            for string in range(1,7):
                if Pos(string,fret) in self.poss:
                    s=s+"o"
                else:
                    s=s+"|"
            s=s+"\n"
        return s
            
