from solfege.interval.alteration import Alteration
from solfege.interval.chromatic import ChromaticInterval
from solfege.interval.diatonic import DiatonicInterval

ChromaticInterval.RelatedDiatonicClass = DiatonicInterval
DiatonicInterval.RelatedChromaticClass = ChromaticInterval
ChromaticInterval.AlterationClass = Alteration