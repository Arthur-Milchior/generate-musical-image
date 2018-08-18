from penalty import Penalty
from note import *
import os
import sys
from util import *
from lily import *
from scales_list import scales


def generateLeftFingeringDic(currentNote,intervals,fingeringDic=None):
    #generated on 2 octaves to check that transition goes smoothly.
    debug("Generating left fingering for %s"%currentNote.getTitleName())
    return generateFingeringDic(currentNote,intervals*2,"left",fingeringDic=fingeringDic)
    
def generateRightFingeringDic(currentNote,intervals,fingeringDic=None):
    return generateFingeringDic(currentNote,intervals*2,"right",fingeringDic=fingeringDic)

def generateFingeringDic(baseNote,intervals,side,fingeringDic=None):
    """Associating to current note and each note of the remaining interval a fingering for  hand whose side is side

    baseNote -- the note where the scale start
    if fingeringDic is a dictionnary from (non-initial) note to fingering. This should be respected in other choice. (normally not used anymore)

    return False if no fingering can be found
    Otherwise, return:
       --the starting finger (lowest for left hand, highest for right hand), 
       --the fingering for the non-star
       , and  
       --the map from other note to finger (probably useless now)
       --the penalty
    """

    fingeringDic=fingeringDic if fingeringDic else dict()
    bestPenalty=None
    for extremalFinger in reversed(range(1,6)):
        debug("Trying extremalFinger %d"%extremalFinger)
        res = generateFingeringDicAux(baseNote,intervals,side, extremalFinger,fingeringDic,isInitial=True)
        if res:
            ((fingeringList,finalFingeringDic),recPenalty)=res
            penalty=recPenalty.addStartingFinger(extremalFinger,data=(extremalFinger,fingeringList,finalFingeringDic))
            if bestPenalty is None or  penalty<bestPenalty:
                debug("The best it is !")
                bestPenalty = penalty
            else:
                debug("The best it is not")
    if bestPenalty is not None:
        return (bestPenalty.data,bestPenalty)
    debug("No correct first finger. Reject\n\n")
    return False
    
def generateFingeringDicAux(currentNote,remainingIntervals,side,currentFinger,fingeringDic,isInitial=True):
    """Associating to current note and each note of the remaining interval a fingering for hand indicated by "side"

    currentNote is the note to which a fingering must be associated
    if currentFinger is None, it is 5 or 4. Otherwise it is the fingering proposed for currentNote
    if fingeringDic is a dictionnary from (non-initial) note to fingering. This should be respected in other choice.
    isInitial state whether we are just starting to generate the scale (in this case, the fingering of the first note should not be added to the dictionnary)

    return False if no fingering can be found
    Otherwise, return:
    --(the fingering for the current intervals(probably useless)
    --the map from non-initial notes to finger)
    --penalty
    """
    if isInitial:
        debug("Initial call to generateFingeringDicAux")
    debug("Note %s with finger %d."%(currentNote.getTitleName(),currentFinger))
    
    currentPair=[(currentNote,currentFinger)]
    if currentNote.isBlack() and currentFinger==1:
        debug("One on black. Reject\n\n")
        return False
    
    noteInBaseoctave = currentNote.baseOctave()
    #debug("note %s, with finger %d in base octave is %s.\n"%(currentNote.debug(),currentFinger,noteInBaseoctave.debug()))
    if isInitial:
        nextFingeringDic = dict(fingeringDic) if fingeringDic else dict()
        if isInitial:
            debug("Initial note, thus not added to dictionnary")
    elif noteInBaseoctave in fingeringDic:
        oldFinger =fingeringDic[noteInBaseoctave]
        debug("%s belongs to fingeringDic. Its old finger is %d."%(currentNote.getTitleName(),oldFinger))
        if currentFinger != oldFinger:
            debug("Old finger %d and current finger %d differs, thus reject."%(oldFinger,currentFinger))
            return False
        else:
            nextFingeringDic=fingeringDic
            debug("Old finger %d and current finger %d are equal, thus accept."%(oldFinger,currentFinger))

            
    else:
        debug("%s does not yet belong to fingeringDic."%currentNote.getTitleName())
        nextFingeringDic = dict(fingeringDic)
        nextFingeringDic[noteInBaseoctave]=currentFinger
        debug(" Added to next fingeringDic.")

    if not remainingIntervals:
        debug("No remaining intervals, thus we return immediatly")
        return ((currentPair,nextFingeringDic),Penalty(endingFinger=currentFinger,data=(currentPair,nextFingeringDic)))
    else:
        debug("Other remaining intervals.")

    (nextDiatonicInterval,nextChromaticInterval)= remainingIntervals[{"left":0,"right":-1}[side]]
    if side=="right":
        nextDiatonicInterval=-nextDiatonicInterval
        nextChromaticInterval=-nextChromaticInterval
    nextDiatonicInterval=Name(nextDiatonicInterval)
    
    nextRemainingIntervals={"left":remainingIntervals[1:],"right":remainingIntervals[:-1]}[side]
    interval=Interval(nextDiatonicInterval,nextChromaticInterval, usingChromaticInterval=True)
    nextNote= currentNote+interval
    localPenalty=Penalty()
    if currentFinger==1:
        if abs(nextDiatonicInterval.di)>1:
            localPenalty=Penalty(thumbTwoDiatonicNote=1)
        elif abs(nextChromaticInterval)>1:
            localPenalty=Penalty(thumbTwoChromaticNote=1)
        if not nextNote.isBlack():
            localPenalty.addThumbWhite()
        nextFingers=[(3,localPenalty),(4,localPenalty),(2,localPenalty)]
    elif currentFinger==2:
        nextFingers=[(1,localPenalty)]
    elif abs(nextDiatonicInterval.di)>1:
        nextFingers=[(currentFinger-1,localPenalty),(currentFinger-2,localPenalty)]
    else:
        nextFingers=[(currentFinger-1,localPenalty)]

    bestPenalty=None
    for nextFinger,penaltyIncrease in nextFingers:
        res = generateFingeringDicAux(nextNote,nextRemainingIntervals,side,nextFinger,nextFingeringDic,isInitial=False)
        if res:
            (fingeringListRec,fingeringDicRec),penaltyRec=res
            penalty=penaltyRec+localPenalty
            penalty.data=({"left":currentPair+fingeringListRec, "right":fingeringListRec+currentPair}[side] ,fingeringDicRec)
            if bestPenalty is None or  penalty<bestPenalty:
                debug("Found new best penalty")
                bestPenalty = penalty
    if bestPenalty is not None:
        debug("Return from note %s"%currentNote.getTitleName())
        return (bestPenalty.data,bestPenalty)
    debug("No correct next finger. Reject\n\n")
    return False
    

def generateLeftFingering(extremalFinger,fingeringDic,currentNote,intervals,nbOctave=1):
    intervals=intervals*nbOctave
    (nextDiatonicInterval,nextChromaticInterval)=intervals[0]
    nextDiatonicInterval=Name(nextDiatonicInterval)
    intervals=intervals[1:]
    currentNote=currentNote.addOctave(-1 if nbOctave==1 else -2)
    nextNote=currentNote+Interval(nextDiatonicInterval,nextChromaticInterval, usingChromaticInterval=True)
    return [(currentNote,extremalFinger)]+generateFingering(nextNote, intervals, fingeringDic)

def generateRightFingering(extremalFinger,fingeringDic,currentNote, intervals,nbOctave=1):
    endNote=currentNote.addOctave(nbOctave)
    intervals=intervals*nbOctave
    intervals=intervals[:-1]
    return generateFingering(currentNote, intervals, fingeringDic)+[(endNote,extremalFinger)]
    

def generateFingering(currentNote,remainingInterval,fingeringDic):
    l=[]
    for (nextDiatonicInterval,nextChromaticInterval) in remainingInterval+[(0,0)]:#adding a last element so the loop is processed once more
        nextDiatonicInterval=Name(nextDiatonicInterval)
        noteInBaseOctave = currentNote.baseOctave()
        finger=fingeringDic[noteInBaseOctave]
        l.append((currentNote,finger))
        currentNote+=Interval(nextDiatonicInterval,nextChromaticInterval, usingChromaticInterval=True)
    return l


doCompile=True 
# scales=[
#     (["Major"],0,0,
#      [2,2,1,2,2,2,1]),
#     # (["Minor harmonic"],3,0,
#     #  [2,1,2,2,1,3,1]),
#     # (["blues"],3,0,
#     #  [(2,3),2,(0,1),1,(2,3),2]),
# ]
root_html="""
<html><head><title>Fingerings of every scales</title></head><body>
<header><h1>Fingerings of every scales</h1></header>
<ul>
"""
with open("anki.csv","w")as anki_file:
  for (scaleNames,nbBemol,nbSharp,intervals) in scales:
    scaleName=scaleNames[0]
    root_html+="""<li><a href='%s'>%s</a></li>"""%(scaleName,scaleName)
    scale_html="""
    <html><head><title>Fingerings of %s</title></head><body>
        <header><h1>Fingerings of %s</h1></header>
    <ul>
    """%(scaleName,scaleName)
    for (baseNote,nbBemol_) in twelve_notes:
        baseNameFile=baseNote.nameForFile()
        baseNameTitle=baseNote.getTitleName()
        scale_html+="""<li><a href='%s'>%s</a></li>"""%(baseNameFile,baseNameTitle)
        scale_note_html="""
        <html><head><title>Fingerings of %s %s</title></head><body>
        <header><h1>Fingerings of %s %s</h1></header>
        <ul>
        """%(baseNameTitle,scaleName,baseNameTitle,scaleName)

        nbSharpFinal= nbSharp-nbBemol_
        nbBemolFinal=nbBemol+nbBemol_
        if nbSharpFinal>nbBemolFinal:
            key=["c","g","d","a","e","b","fis","cis","gis","dis","ais","eis","bis"][nbSharpFinal]
        else:
            key=["c","f","bes","ees","aes","des","ges","ces","fes","beses","eeses","aeses", "deses", "ceses", "feses"][nbBemolFinal]
        debug("%s has %d bemol, %s has %d bemol and %d sharp.\nTotal is %d bemol and %d sharp.\nThe key is %s." %(baseNote.getTitleName(),nbBemol_,scaleName,nbBemol,nbSharp, nbSharpFinal, nbBemolFinal,key))
        folder_scale="piano_scales/%s"%(scaleName)
        folder_scale_note="%s/%s"%(folder_scale,baseNameFile)
        ensureFolder(folder_scale_note)
        anki_file.write("\n%s,%s"%(scaleName,baseNameFile))
        if doCompile:
            leftFingeringDic=generateLeftFingeringDic(baseNote, intervals)
            rightFingeringDic=generateRightFingeringDic(baseNote, intervals)
            if not leftFingeringDic or not rightFingeringDic:
                print("Warning:%s %s can't exist !!!\n\n\n"%(scaleName,baseNote.getTitleName()), file=sys.stderr)
                continue
            ((leftExtremalFinger,_,leftFingeringDic),penaltyLeft)=leftFingeringDic
            ((rightExtremalFinger,_,rightFingeringDic),penaltyRight)=rightFingeringDic
            if not penaltyRight.acceptable():
                print("Warning:Right is not perfect on %s %s.\n%s"%(baseNote.getTitleName(),scaleName,penaltyRight.warning()), file=sys.stderr)
            if not penaltyLeft.acceptable():
                print("Warning:Left is not perfect on %s %s.\n\n%s"%(baseNote.getTitleName(),scaleName,penaltyLeft.warning()), file=sys.stderr)
        for nbOctave in [1,2,
                         3,
                         4,
                        ]:
            if doCompile:
                leftIncreasing=generateLeftFingering(leftExtremalFinger,leftFingeringDic,baseNote,intervals, nbOctave=nbOctave)
                rightIncreasing=generateRightFingering(rightExtremalFinger,rightFingeringDic,baseNote,intervals, nbOctave=nbOctave)
            else:
                leftIncreasing=[42]
                rightIncreasing=[42]
            leftDecreasing=list(reversed(leftIncreasing))
            rightDecreasing=list(reversed(rightIncreasing))
            for kind,leftFingering,rightFingering in[("increasing",leftIncreasing,rightIncreasing),
                                                     ("decreasing",leftDecreasing,rightDecreasing),
                                                     ("total",leftIncreasing[:-1]+leftDecreasing,rightIncreasing[:-1]+rightDecreasing),
                                                     ("reverse",leftDecreasing[:-1]+leftIncreasing,rightDecreasing[:-1]+rightIncreasing)
            ]:
                localLilySide = lilySide if doCompile else (lambda x, y, z : 42)
                localLilyBoth = lilyBoth if doCompile else (lambda x, y, z : 42)
                for hand,lilyCode in [
                        ("left",localLilySide(key,leftFingering,"left")),
                        ("right",localLilySide(key,rightFingering,"right")),
                        ("both",localLilyBoth(key, leftFingering,rightFingering))
                ]:
                    fileName="%s-%s-%s-%d-%s"%(scaleName,baseNameFile,hand,nbOctave,kind)
                    anki_file.write(",<img src='%s.png'>"%fileName)
                    if nbOctave>2 or  not doCompile:
                        continue
                    folder_fileName ="%s/%s"%(folder_scale_note,fileName)
                    folder_fileName_ly =folder_fileName+".ly"
                    folder_fileName_png=folder_fileName+".png"
                    scale_note_html+="""<li><img src='%s.svg'/></li>"""%(fileName)
                    if os.path.isfile(folder_fileName_ly):
                        debug("%s already exists."%(folder_fileName_ly))
                        with open(folder_fileName_ly) as file:
                            last_code = file.read()
                            if last_code!= lilyCode:
                                debug("Code is distinct, we rewrite")
                                compile=True
                            else:
                                debug("same code. We do nothing")
                                compile=False
                    else:
                        compile=True
                    if compile:                    
                        print("%s should be generated."%(folder_fileName_png))
                        with open(folder_fileName_ly, "w") as file:
                            file.write(lilyCode)
                        os.system("""/home/milchior/bin/lilypond -dbackend=svg -o "%s"  "%s" """%(folder_fileName,folder_fileName_ly))
                        # os.system("""inkscape --verb=FitCanvasToDrawing --verb=FileSave --verb=FileClose "%s.svg"&"""%(folder_fileName))
                        # os.system("""pkill inkscape""")
                        #os.system("""/home/milchior/bin/lilypond  -o "%s" "%s" """%(folder_fileName,folder_fileName_ly))
                        #os.system("""convert -background "#FFFFFF" -flatten "%s.svg" "%s.png" """%(folder_fileName,folder_fileName))
        scale_note_html+="""</ul>
        <footer>
        <a src="../../about.html"/>About</a><br/>
        <a href='../..'>Other scales</a><br/>
        <a href='..'>Other note of this scale</a>
        </footer>
        </body>
        </html>
        """
        with open("%s/index.html"%folder_scale_note,"w") as scale_note_file:
            scale_note_file.write(scale_note_html)
        
    scale_html+="""</ul>
    <footer>
    <a src="../../about.html"/>About</a><br/>
    <a href='..'>Other scales</a>
    </footer>
    </body>
    </html>
    """
    with open("%s/index.html"%folder_scale,"w") as scale_file:
        scale_file.write(scale_html)
        
root_html+="""
</ul>
<footer><a src="about.html"/>About</a></footer>
</body>
</html>
"""
with open("piano_scales/index.html","w") as html_file:
    html_file.write(root_html)
with open("piano_scales/about.html","w") as html_file:
    html_file.write("""
<html><head><title>About fingerings of every scales</title></head><body>
Author: <a href="mailto:arthur@milchior.fr"/>Arthur Milchior</a>. Don't hesitate to contact me with idea about improving this set of fingerings. Or edit it yourself in <a href='https://github.com/Arthur-Milchior/generate-musical-image'/>git-hub</a>.

<p>
    The list of scales is mostly taken from the <a href='https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes'/>wikipedia's list of scale</a> and from the pages linked by it. Only scales which can be played on a keyboard (12 fingers by octave) have been considered. </p>

    <p>When multiple fingerings are possible, the "best" one is generated as follows:<ol>
    <li>
    No thumb ever play a black key.
    </li>
    <li>
    As far as possible, after a thumb over, the next note played is the one following in the diatonic scale.  </li>
    <li>The number of thumb over is minimal, with respect to previous condition </li>
    <li>
    The lowest finger on left hand (highest on right hand) is as high as possible (i.e. 5 if possible, otherwise, 4, etc..).
    </li>
    <li>
    The highest finger on left hand (lowest on right hand) is as low as possible. (i.e. thumb if possible)
    </li>
    <li>
    As far as possible, a thumb passing goes to a black key and not a white one.
    </li>
    <li>
    As far as possible, a thumb passing goes to a key whose chromatic distance is one.
    </li>
<ol>

</body></html>
    """)
