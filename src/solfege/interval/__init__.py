from solfege.interval.intervalmode import IntervalMode
from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval

ChromaticInterval.RelatedDiatonicClass = DiatonicInterval
DiatonicInterval.RelatedChromaticClass = ChromaticInterval
ChromaticInterval.AlterationClass = IntervalMode
