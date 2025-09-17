from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern, IntervalListPattern
from solfege.pattern.chord.chord_patterns import major_triad

major_chromatic_interval_list_and_its_inversion = IdenticalInversionPatterns(
    intervals=IntervalListPattern.make_absolute([(0,0), (4, 2), (7, 4)]),
    inversion_patterns = [major_triad.inversion(0)]
    )