#It should generate:
#63 scales
#12 note
#2 octaves
#4 kinds
#3 hands
#=18144 images
#Taking 4 seconds each, it takes 20 hours

from .penalty import Penalty
from .note import Note
from solfege.interval import SolfegeInterval
from util import *
from .lily import *
lilyProgram="lilypond "

class Fingering:
    def __init__(self):
        self.dic=dict()
        self.baseNote=None
        self.baseFinger=None

    def copy(self):
        nex=Fingering()
        nex.baseNote=self.baseNote
        nex.baseFinger=self.baseFinger
        nex.dic=dict(self.dic)
        return nex

    def __contains__(self,note):
        note=note.baseOctave()
        return note in self.dic
    
    def add(self,note,finger):
        """True if adding was useless, because the note is already there.
        False if adding contradicts the note already in the dic
        A new fingering, similar to self, with this note added otherwise"""
        nex=self.copy()
        note=note.baseOctave()
        if self.baseNote is None:
            nex.baseNote =note
            nex.baseFinger=finger
        else:
            if note in nex.dic:
                return nex.dic[note]==finger
            nex.dic[note]=finger
        return nex

    def isEndEqualStart(self):
        return self.getLastFinger()==self.baseFinger

    def isEnd1(self):
        return self.getLastFinger()==1

    def isEndNice(self):
        return self.isEnd1() or self.isEndEqualStart()

    def getLastFinger(self):
        return self.get(self.baseNote)

    def get(self,note,base=False):
        note=note.baseOctave()
        if base:
            if note!=self.baseNote:
                raise Exception("Not the correct base not")
            else:
                return self.baseFinger
        return self.dic[note]

    
def generateLeftFingeringDic(currentNote,intervals,fingeringDic=None):
    debug("Generating left fingering for %s",currentNote.getName())
    intervals= intervals+[intervals[0]]
    return generateFingeringDic(currentNote,intervals,"left",fingeringDic=fingeringDic)
    
def generateRightFingeringDic(currentNote,intervals,fingeringDic=None):
    intervals=[intervals[-1]]+intervals
    return generateFingeringDic(currentNote,intervals,"right",fingeringDic=fingeringDic)

def generateFingeringDic(baseNote,intervals,side,fingeringDic=None):
  """Associating to current note and each note of the remaining interval a fingering for  hand whose side is side

  baseNote -- the note where the scale start
  if fingeringDic is a dictionnary from (non-initial) note to fingering. This should be respected in other choice. (normally not used anymore)

  return False if no fingering can be found
  Otherwise, return:
     --the starting finger (lowest for left hand, highest for right hand), 
     --the fingering for the non-star
     , and  
     --the penalty
  """
  def aux(currentNote,remainingIntervals,side,currentFinger,fingeringDic,isInitial=True):
    """Associating to current note and each note of the remaining interval a fingering for hand indicated by "side"

    currentNote is the note to which a fingering must be associated
    if currentFinger is None, it is 5 or 4. Otherwise it is the fingering proposed for currentNote
    if fingeringDic is a dictionnary from (non-initial) note to fingering. This should be respected in other choice.
    isInitial state whether we are just starting to generate the scale (in this case, the fingering of the first note should not be added to the dictionnary)

    return False if no fingering can be found
    Otherwise, return:
    --the map from non-initial notes to finger)
    --penalty
    """
    if isInitial:
        debug("Initial call to aux")
    #debug("Note %s with finger %d.",(currentNote.getName(),currentFinger))
    
    if currentNote.isBlack() and currentFinger==1:
        debug("One on black. Reject\n\n")
        return False
    
    #debug("note %s, with finger %d in base octave is %s.\n",(currentNote.debug(),currentFinger,noteInBaseoctave.debug()))
    nextFingeringDic = fingeringDic.add(currentNote,currentFinger)
    if nextFingeringDic is False:
        return False
    if nextFingeringDic is True:
        nextFingeringDic=fingeringDic
    if not remainingIntervals:
        debug("No remaining intervals, thus we return immediatly")
        endingFinger=nextFingeringDic.getLastFinger()
        niceExtremity=nextFingeringDic.isEndNice()
        penalty=Penalty(endingFinger=endingFinger,niceExtremity=niceExtremity,data=nextFingeringDic)
        return (nextFingeringDic,penalty)

    (nextDiatonicInterval,nextChromaticInterval)= remainingIntervals[{"left":0,"right":-1}[side]]
    if side=="right":
        nextDiatonicInterval=-nextDiatonicInterval
        nextChromaticInterval=-nextChromaticInterval
    
    nextRemainingIntervals={"left":remainingIntervals[1:],"right":remainingIntervals[:-1]}[side]
    interval=SolfegeInterval(nextChromaticInterval,nextDiatonicInterval)
    nextNote= currentNote+interval
    #debug("With note %s and interval %s we obtain note %s",(currentNote,interval,nextNote))
    localPenalty=Penalty()
    if currentFinger==1:
        if not baseNote.distinctOctave(currentNote):
            localPenalty=localPenalty.addPassingFinger()
        if not currentNote.adjacent(nextNote):
            localPenalty=localPenalty.addThumbNonAdjacent()
        if not nextNote.isBlack():
            localPenalty=localPenalty.addWhiteAfterThumb()
        nextFingers=[3,4,2]
    elif currentFinger==2:
        nextFingers=[1]
    elif abs(nextDiatonicInterval)>1:
        nextFingers=[currentFinger-1,currentFinger-2]
    else:
        nextFingers=[currentFinger-1]

    bestPenalty=None
    for nextFinger in nextFingers:
        res = aux(nextNote,nextRemainingIntervals,side,nextFinger,nextFingeringDic,isInitial=False)
        if res:
            fingeringDicRec,penaltyRec=res
            sumPenalty=penaltyRec+localPenalty
            sumPenalty.data=fingeringDicRec
            if bestPenalty is None or  sumPenalty<bestPenalty:
                debug("Found new best penalty")
                bestPenalty = sumPenalty
    if bestPenalty is not None:
        debug("Return from note %s",currentNote.getName())
        return (bestPenalty.data,bestPenalty)
    debug("No correct next finger. Reject\n\n")
    return False
  ##End aux
  fingeringDic=fingeringDic if fingeringDic else Fingering()
  bestPenalty=None
  for extremalFinger in reversed(range(1,6)):
      debug("Trying extremalFinger %d",extremalFinger)
      res = aux(baseNote,intervals,side, extremalFinger,fingeringDic,isInitial=True)
      if res:
          (finalFingeringDic,recPenalty)=res
          penalty=recPenalty.addStartingFinger(extremalFinger,data=(extremalFinger,finalFingeringDic))
          if bestPenalty is None or  penalty<bestPenalty:
              debug("The best it is !")
              bestPenalty = penalty
          else:
              debug("The best it is not")
  if bestPenalty is not None:
      return (bestPenalty.data,bestPenalty)
  debug("No correct first finger. Reject\n\n")
  return False
    
    

def generateLeftFingering(extremalFinger,fingeringDic,baseNote,intervals,nbOctave=1):
    debug("Generate left fingering, starting on note note %s",baseNote)
    intervals=intervals*nbOctave
    (nextDiatonicInterval,nextChromaticInterval)=intervals[0]
    intervals=intervals[1:]
    baseNote=baseNote.addOctave(-1 if nbOctave==1 else -2)
    interval=SolfegeInterval(nextChromaticInterval,nextDiatonicInterval)
    nextNote=baseNote+interval
    debug("When adding %s, we obtain %s",(interval,nextNote))
    return [(baseNote,extremalFinger)]+generateFingering(nextNote, intervals, fingeringDic)

def generateRightFingering(extremalFinger,fingeringDic,baseNote, intervals,nbOctave=1):
    endNote=baseNote.addOctave(nbOctave)
    intervals=intervals*nbOctave
    intervals=intervals[:-1]
    return generateFingering(baseNote, intervals, fingeringDic)+[(endNote,extremalFinger)]
    

def generateFingering(currentNote,remainingInterval,fingeringDic):
    debug("Starting generate fingering. Current note is %s",currentNote)
    l=[]
    for (nextDiatonicInterval,nextChromaticInterval) in remainingInterval+[(0,0)]:#adding a last element so the loop is processed once more
        finger=fingeringDic.get(currentNote)
        l.append((currentNote,finger))
        currentNote+=SolfegeInterval(nextChromaticInterval,nextDiatonicInterval)
        debug("Next note is %s",currentNote)
    return l


