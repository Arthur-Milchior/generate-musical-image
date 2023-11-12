import lily.lily
from guitar.pos import SetOfPos, Pos
from solfege.chords import ChordPattern
from solfege.interval import ChromaticInterval
from solfege.note import Note
from solfege.note.with_tonic import ChromaticNoteWithTonic
from util import debug
from .util import minNumberString


class PosWithBase(Pos, ChromaticNoteWithTonic):
    pass


class SetOfIntervals:
    def __init__(self, set_=None):
        self.set_ = set()
        self.set_base_octave = set()
        if set_:
            for interval in set_:
                self.set_.add(interval)
                self.set_base_octave.add(interval.get_same_note_in_base_octave())

    def __contains__(self, interval):
        return interval.get_same_note_in_base_octave() in self.set_base_octave

    def __iter__(self):
        return iter(self.set_base_octave)


class GuitarChord(SetOfPos):
    """A chord. That is, a fret by string. 0 for empty string"""

    def __init__(self, dic):
        # {string:fret for string,fret in dic.items () if fret is not None}
        self.chord = [PosWithBase(i + 1, dic[i]) for i in range(0, 6)]
        self.numberChord = len([1 for i in dic if i is not None])
        # {Pos(string,fret) for string,fret in dic.items ()}
        super().__init__(self.chord)
        minPos = self.getMinPos()
        for chord in self.chord:
            chord.set_base(minPos)
        self.setOfInterval = SetOfIntervals(
            {chord.get_interval() for chord in self.chord if chord.get_interval() is not None})

    def anki(self):
        """return the tuple (pos1,pos3,pos5,posn)

        pos1 is the string of length 6, whose x represents a string not played, . a string played, but not for note tonic, and 1 represents a string played for the tonic.
        pos3, pos5  are similar for third and fifth. posn is used for 6th or 7th
        """
        text = ""
        for (number, setOfInterval) in [("1", {ChromaticInterval(0)}),
                                        ("3", {ChromaticInterval(3), ChromaticInterval(4)}),
                                        ("5", {ChromaticInterval(6), ChromaticInterval(7)}),
                                        ("n", {ChromaticInterval(9), ChromaticInterval(10), ChromaticInterval(11)})]:
            text += ","
            for i in self.chord:
                interval = self.chord[i].get_interval()
                if interval is None:
                    text += "x"
                else:
                    if interval in setOfInterval:
                        text += number
                    else:
                        text += "."
        return text

    def getPosFromString(self, string):
        """The pos corresponding to the chord number i"""
        return self.chord[string - 1]

    def fileNameBase(self):
        if "fileNameBase" not in self.dic:
            text = ""
            for i in range(1, 7):
                fret = self.getPosFromString(i).fret
                if fret is None:
                    text += "x"
                elif isinstance(fret, int):
                    text += str(fret)
                else:
                    raise Exception("Fret is neither None, nor an int, but %s", fret)
            self.dic["fileNameBase"] = text
            debug("its file base name is:%s" % text)
        return self.dic["fileNameBase"]

    def fileName(self):
        return self.fileNameBase()

    def playable(self):
        """At most three frets not being on fret 0 or 1"""
        if "playable" not in self.dic:
            playable = True
            nbGtOne = 0  # nb of fret >1 played.
            nbOne = 0  # nb of fret 1 played
            m = 12  # least non 0 fret played
            M = -1  # greatest fret played
            for pos in self.poss:
                if pos.fret is None:
                    raise Exception
                if pos.fret > 0:
                    m = min(m, pos.fret)
                M = max(M, pos.fret)
                if pos.fret == 1:
                    nbOne += 1
                if pos.fret > 1:
                    nbGtOne += 1

            if M - m > 4:
                debug("More than four fret of difference between bottom and top")
                playable = False
            elif self.isOpen():
                if nbGtOne + nbOne > 4:
                    debug("Open string and %d elements which are >0" % (nbGtOne + nbOne))
                    playable = False
            else:  # not open chord
                if nbGtOne > 3:
                    debug("Closed string and %d elements which are >1" % nbGtOne)
                    playable = False
            self.dic["playable"] = playable
            debug("is its playable:%s" % playable)
        return self.dic["playable"]

    def enoughStrings(self):
        r = self.numberChord >= minNumberString
        if r:
            debug("At least %d string" % minNumberString)
            return True
        else:
            debug("Only %d strings played" % self.numberChord)
            return False

    def isChord(self):
        """Whether this is both a stanad chord, with 4 notes, and can actually be played"""
        return self.isStandardChord() and self.playable() and self.enoughStrings()

    def isOpenChord(self):
        """whether one string is played open, and it is actually a chord"""
        if "isOpenChord" not in self.dic:
            r = self.isOpen() and self.isChord()
            self.dic["isOpenChord"] = r
            debug("is it an open chord:%s" % r)
        return self.dic["isOpenChord"]

    def isTransposableChord(self):
        """whether it is a chord, and its minimal element is one"""
        if "isTransposableChord" not in self.dic:
            r = self.isOneMin() and self.isStandardChord() and self.playable() and self.enoughStrings()
            self.dic["isTransposableChord"] = r
            debug("is it a transposable chord:%s" % r)
        return self.dic["isTransposableChord"]

    # def isAcceptable(self):
    #     """Whether its a chord I want to consider"""
    #     if "isAcceptable" not in self.dic:
    #         r=(self.containsTonic() or self.isOpen()) and self.isChord()
    #         self.dic["isAcceptable"]=r
    #         debug("is it acceptable chord:%s"% r)
    #     return self.dic["isAcceptable"]

    def inChordsList(self):
        return True if ChordPattern.getFromInterval(self.setOfInterval) else False

    def kind(self):
        """transposable(1 as first string), open, or None"""
        if "kind" not in self.dic:
            if self.isOpen():
                r = "open"
            elif self.isOneMin():
                r = "transposable"
            else:
                r = None
            self.dic["kind"] = r
            debug("its kind is:%s" % r)
        return self.dic["kind"]

    # def __str__(self):
    #     return self.name()
    # return str(SetOfPos(self))
    # def __init__(self, base, quality, interval, renversement, string, fret):
    # self.base = base
    # self.quality = quality
    # self.interval = interval
    # self.renversement = renversement
    # self.string = string
    # self.fret = fret

    # class SetOfInterval:
    #     """The set of chromatic interval between the notes and the lowest note"""
    #     def __init__(self, sop):
    def isMinor(self):
        if "isMinor" not in self.dic:
            r = ChromaticInterval(3) in self.setOfInterval
            self.dic["isMinor"] = r
            debug("is it minor:%s" % r)
        return self.dic["isMinor"]

    def containsTonic(self):
        if "containsTonic" not in self.dic:
            r = ChromaticInterval(0) in self.setOfInterval
            self.dic["containsTonic"] = r
            debug("Does it contains tonic:%s" % r)
        return self.dic["containsTonic"]

    def isMajor(self):
        if "isMajor" not in self.dic:
            r = ChromaticInterval(4) in self.setOfInterval
            self.dic["isMajor"] = r
            debug("is it major:%s" % r)
        return self.dic["isMajor"]

    def getSetOfNote(self):
        """return the set of note (i.e. no repetition)"""
        setNote = set()
        setPos = set()
        for chord in self.chord:
            assert (isinstance(chord, PosWithBase))
            if chord.fret is not None:
                chromatic = chord.getChromatic()
                assert (isinstance(chord, ChromaticNoteWithBase))
                note = chromatic.get_note()
                assert (isinstance(note, Note))
                if note not in setNote:
                    setPos.add(chord)
                    setNote.add(note)
        return setPos

    def lily(self, color=True):
        return lily.lily.chord(self.getSetOfNote(), color=color)

    def third(self):
        """The kind of third of this chord, or False"""
        if "third" not in self.dic:
            if self.isMinor():
                if self.isMajor():
                    self.dic["third"] = False
                else:
                    self.dic["third"] = "min"
            elif self.isMajor():
                self.dic["third"] = "Maj"
            else:
                self.dic["third"] = False
            debug("Its third is: %s" % self.dic["third"])
        return self.dic["third"]

    def isFifthDimished(self):
        if "isFifthDimished" not in self.dic:
            r = ChromaticInterval(6) in self.setOfInterval
            self.dic["isFifthDimished"] = r
            debug("is it fifth diminished:%s" % r)
        return self.dic["isFifthDimished"]

    def isFifthAugmented(self):
        if "isFifthAugmented" not in self.dic:
            r = ChromaticInterval(8) in self.setOfInterval
            self.dic["isFifthAugmented"] = r
            debug("is it fifth diminished:%s" % r)
        return self.dic["isFifthAugmented"]

    def isFifthJust(self):
        if "isFifthJust" not in self.dic:
            r = ChromaticInterval(7) in self.setOfInterval
            self.dic["isFifthJust"] = r
            debug("is it fifth just:%s" % r)
        return self.dic["isFifthJust"]

    def fifth(self):
        """If the 5th is diminished, and third is minor return "diminished".
        If the 5th is just, return the empty string.
        Otherwise return false
        """
        if "fifth" not in self.dic:
            augmented = self.isFifthAugmented()
            diminished = self.isFifthDimished()
            just = self.isFifthJust()
            numberFifth = len([fifth for fifth in [just, diminished, augmented] if fifth])
            if numberFifth == 0:
                self.dic["fifth"] = None
            elif numberFifth > 1:
                self.dic["fifth"] = False
            elif diminished:
                if self.is7thMaj() or self.is7thMin():
                    self.dic["fifth"] = False
                else:
                    self.dic["fifth"] = "diminished"
            elif just:
                self.dic["fifth"] = "just"
            elif augmented:
                if self.is6th() or self.is7thMin():
                    self.dic["fifth"] = False
                else:
                    self.dic["fifth"] = "augmented"
            debug("The fifth is %s" % self.dic["fifth"])
        return self.dic["fifth"]

    def hasNoQuality(self):
        """Whether there is no 6th nor 7th"""
        return not self.hasQuality()

    def hasQuality(self):
        """Whether there is no 6th nor 7th"""
        if "hasQuality" not in self.dic:
            r = (self.is6th() or self.is7thMin() or self.is7thMaj())
            self.dic["hasQuality"] = r
            debug("Does it has quality:%s" % r)
        return self.dic["hasQuality"]

    def is6th(self):
        if "has6th" not in self.dic:
            r = ChromaticInterval(9) in self.setOfInterval
            self.dic["has6th"] = r
            debug("Does it has a 6th:%s" % r)
        return self.dic["has6th"]

    def is7thMin(self):
        if "has7thMin" not in self.dic:
            r = ChromaticInterval(10) in self.setOfInterval
            self.dic["has7thMin"] = r
            debug("Does it has a 7thMin:%s" % r)
        return self.dic["has7thMin"]

    def is7thMaj(self):
        if "has7thMaj" not in self.dic:
            r = ChromaticInterval(11) in self.setOfInterval
            self.dic["has7thMaj"] = r
            debug("Does it has a 7thMaj:%s" % r)
        return self.dic["has7thMaj"]

    def quality(self):
        """The quality of the chord. False if it has multiple potential note which can be considered as distinct quality."""
        if "quality" not in self.dic:
            sixth = self.is6th()
            seventhMinor = self.is7thMin()
            seventhMajor = self.is7thMaj()
            numberQuality = len([quality for quality in [sixth, seventhMajor, seventhMinor] if quality])
            if numberQuality == 0:
                r = ""
            elif numberQuality > 1:
                r = False
            elif sixth:
                r = "6"
            elif seventhMinor:
                r = "7min"
            elif seventhMajor:
                r = "7maj"
            else:
                r = None
            self.dic["quality"] = r
            debug("Its quality is:%s" % r)
        return self.dic["quality"]

    def anki(self):
        """A string containing the kind of Third, of fifth, and of quality"""
        return "%s,%s,%s" % (self.third(), self.fifth(), self.quality())

    def contains567(self):
        """Whether it has a fifth or a quality"""
        if "hasQualityOr5" not in self.dic:
            r = (self.fifth() or self.quality())
            self.dic["hasQualityOr5"] = r
            debug("Does it has quality or fifth:%s" % r)
        return self.dic["hasQualityOr5"]

    def containsWrongNote(self):
        """Whether it contains an interval which should not be present in a standard reversed chord"""
        if "wrong note" not in self.dic:
            r = False
            if ChromaticInterval(1) in self.setOfInterval:
                debug("Contains half tone")
                r = True
            if ChromaticInterval(2) in self.setOfInterval:
                debug("Contains tone")
                r = True
            if ChromaticInterval(5) in self.setOfInterval:
                debug("contains fourth")
                r = True
            self.dic["wrong note"] = r
            debug("Does it contains a wrong note: %s" % r)
        return self.dic["wrong note"]

    def isStandardChord(self):
        """Given a set of notes, is it a standard chord. I.e.:
        -has a tonic
        -has a third
        -has a fifth diminshed only if its third is minor
        -has either a fifth or a quality
        """
        if "standard" not in self.dic:
            r = True
            if self.containsWrongNote():
                debug("Contains wrong note")
                r = False
            if not self.third():
                debug("Has no third")
                r = False
            if self.fifth() is False:
                debug("Contains too much fifth. Or a 7th with a fifth diminshed")
                r = False
            if self.quality is False:
                debug("wrong quality")
                r = False
            if not self.containsTonic():
                debug("has no tonic")
                r = False
            if not self.contains567():
                debug("Has no interval at least 5th")
                r = False
            self.dic["standard"] = r
            debug("Is it standard chord:%s" % r)
        return self.dic["standard"]

    def isNonStandard(self):
        return not self.isStandardChord()

    def reversed(self):
        """if this chord is a reversed chord of a chord without 6th, then returns this tonic, otherwise None """
        for ht in self.s:
            transposed = {ht_ % 12: ht_ in self.s}
            if isStandardChord(transposed) and ht < m and (not is6th(transposed)):
                return transposed
        return None

    def getPatternName(self):
        if "pattern name" not in self.dic:
            chord = ChordPattern.getFromInterval(self.setOfInterval)
            if chord is None:
                self.dic["pattern name"] = None
            else:
                self.dic["pattern name"] = chord.get_the_first_of_the_name()
            debug("Pattern name is %s" % self.dic["pattern name"])
            self.dic["pattern name"]
        return self.dic["pattern name"]

    def getReallyDescriptiveName(self, withKind=True):
        """Name of chord, assuming it is standard"""
        if "descriptiveName" not in self.dic:
            if self.isFifthDimished():
                fifthName = "-Dim"
            elif self.isFifthAugmented():
                fifthName = "-Aug"
            else:
                # if self.isFifthJust():
                fifthName = ""
            # else:
            #     fifthName = "-None"
            qualityName = self.quality()
            if qualityName:
                qualityName = "-%s" % qualityName
            if qualityName == "-6" and self.isFifthDimished():
                qualityName = "-dim7"
                fifthName = ""
            if qualityName == "-7maj" and self.isFifthAugmented():
                qualityName = "-7"

            if withKind:
                if self.isOpen():
                    pos = "open-" + self.getMinPos().name() + "-"
                else:
                    pos = "transposable-"
            else:
                pos = ""
            name = "%s%s%s%s" % (pos, self.third(), fifthName, qualityName)
            debug("descriptiveName is %s" % name)
            self.dic["descriptiveName"] = name
        return self.dic["descriptiveName"]
