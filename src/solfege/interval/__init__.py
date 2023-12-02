from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval
from solfege.interval.intervalmode import IntervalMode

ChromaticInterval.RelatedDiatonicClass = DiatonicInterval
DiatonicInterval.RelatedChromaticClass = ChromaticInterval
ChromaticInterval.AlterationClass = IntervalMode
