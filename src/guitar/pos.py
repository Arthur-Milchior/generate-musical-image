from io import StringIO

from solfege.note import ChromaticNote


class Pos(ChromaticNote):


    def __str__(self):
        if isinstance(self.fret, int):
            return "(%d,%d)" % (self.string, self.fret)
        elif self.fret is None:
            return "(%d,x)" % self.string
        else:
            raise

    def __repr__(self):
        return "Pos(%d,%d)" % (self.string, self.fret)

    def __lt__(self, pos):
        return (pos is None or
                (self.getChromatic() < pos.getChromatic()) or
                (self.getChromatic() == pos.getChromatic() and self.string < pos.string))

    def __eq__(self, pos):
        return self.string == pos.string and self.fret == pos.fret

    def __hash__(self):
        chroma = self.getChromatic()
        if chroma is None:
            return -100
        return chroma.get_number()

    def _draw(self, f, color=True):
        f.write(self.svg(color))

    def getFillColor(self):
        if self.fret == 0:
            return "white"
        else:
            return "black"

    def __sub__(self, pos):
        if isinstance(pos, Pos):
            return self.subPos(pos)
        else:
            return self.sub_interval(pos)

    def subPos(self, pos):
        """the number of semitone from self (high note) to pos (low note)"""
        if self.fret is None:
            raise Exception("Trying to substract from a non played string %s" % self)
        return self.getChromatic() - pos.get_chromatic()

    def add(self, interval, min=0, max=5):
        """A pos, equal to self, with `interval`  semitone added

        fret is minimal in [min,max]. If no such pos exists, return None

        interval -- a chromatic interval
        """
        chromaticResult = self.getChromatic() + interval
        assert isinstance(chromaticResult, ChromaticNote)
        max_string = None
        for string in string_number_to_distance_from_C4:
            if min <= (chromaticResult - string_number_to_distance_from_C4[string]).get_number() <= max:
                if (max_string is None) or (string > max_string):
                    max_string = string
        if max_string:
            return Pos(max_string, (chromaticResult - string_number_to_distance_from_C4[max_string]).get_number())
        else:
            return None

    def toSop(self):
        """A set of pos whose only element is this position."""
        return SetOfPos({self})

    def draw(self, f, nbFretMin=3):
        """Draw a fret with this only position"""
        self.toSop().draw(f, nbFretMin=nbFretMin)

    # def name(self,withOctave=False): #todo:replace by getnotname
    #     """The name of this position. Assuming standard guitar"""
    #     return self.getChromatic().getNoteName(withOctave=withOctave)


class SetOfPos:
    """A set of position of the guitar"""

    def __init__(self, poss, silences={}):
        """Poss-a set of pos

        poss -- a set of position
        maxFret -- the maximal fret in the set
        minFret -- the minimal fret in the set
        containsFirstFret -- whether the first fret is present
        minPos -- the position of the lowest note
        silences -- a set of strings which should not be played

        """
        assert (len(poss))
        self.poss = set()
        self.maxFret = -1
        self.minFret = 100
        self.containsFirstFret = False
        self.minPos = None
        self.silences = set(silences)
        for pos in poss:
            if pos.fret is None:
                self.silences.add(pos.string)
                continue
            self.poss.add(pos)
            if pos.fret == 1:
                self.containsFirstFret = True
            self.maxFret = max(self.maxFret, pos.fret)
            self.minFret = min(self.minFret, pos.fret)
            if self.minPos is None or pos < self.minPos:
                self.minPos = pos
        self.dic = dict()

    def __iter__(self):
        """Iterator over the positions"""
        return iter(self.poss)

    def __lt__(self, sop):
        """Whether each pos of this Pos belong to sop, except maybe from empty string position.

        sop -- another set of position."""
        for pos in self.poss:
            if pos.fret is not None and pos not in sop.poss:
                return False
        return True

    def isOneMin(self):
        """ Whether there is a first fret played. """
        if "isOneMin" not in self.dic:
            r = self.containsFirstFret and not self.isOpen()
            self.dic["isOneMin"] = r
        return self.dic["isOneMin"]

    def isOpen(self):
        """Whether there is a note played free."""
        if "isOpen" not in self.dic:
            r = self.minFret == 0
            self.dic["isOpen"] = r
        return self.dic["isOpen"]

    def getMaxFret(self):
        return self.maxFret

    def getMinPos(self):
        minPos = self.minPos
        assert (minPos)
        return minPos

    def draw(self, f, nbFretMin=0, color=True):
        f.write(self.svg(nbFretMin, color))

    def svg(self, nbFretMin=0, color=True):
        """Some svg text showing the fret and each of its position.

        nbFretMin -- at least this number of fret are shown. Maybe more if necessary"""
        f = StringIO()
        nbFretToDraw = max(self.maxFret, nbFretMin)
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:d}" height="{height:d}" version="1.1">""")
        for i in range(1, 7):
            # columns
            x = string_distance * (i - .5)
            y1 = fret_distance / 2
            y2 = fret_distance * (nbFretToDraw + .5)
            f.write("""
  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />""" % (x, y1, x, y2))
        for i in range(1, nbFretToDraw + 2):
            # lines
            x1 = string_distance / 2
            x2 = string_distance * 5.5
            y = fret_distance * (i - .5)
            f.write("""
  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />""" % (x1, y, x2, y))

        for pos in self.poss:
            pos._draw(f, color=color)
        for string in self.silences:
            Pos(string, None)._draw(f, color=color)
        f.write("""
</svg>""")
        return f.getvalue()

    def tab(self):
        if self.maxFret == -1:
            return """
||||||
Empty Fret
||||||"""
        # s = "{"
        # for pos in self.s:
        #     s += str(pos)+","
        # s+="}"
        # return s
        s = "\n"
        # pair = [pos.string,pos.fret for pos in self.s]
        for string in range(1, 7):
            if Pos(string, 0) in self.poss:
                s = s + "o"
            elif string in self.silences:
                s = s + "x"
            else:
                s = s + " "
        s = s + "\n"
        for fret in range(1, self.maxFret + 1):
            for string in range(1, 7):
                if Pos(string, fret) in self.poss:
                    s = s + "•"
                else:
                    s = s + "|"
            s = s + "\n"
        return s

    def __repr__(self):
        return "\n%s\n" % self.tab()
