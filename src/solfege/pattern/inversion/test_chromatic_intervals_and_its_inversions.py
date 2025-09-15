from solfege.pattern.inversion.identical_inversion_patterns import IdentiticalInversionPatterns
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from solfege.pattern.chord.chord_patterns import major_triad

major_chromatic_interval_list_and_its_inversion = IdentiticalInversionPatterns(
    chromatic_intervals=ChromaticIntervalListPattern.make_absolute([0, 4, 7]),
    inversions = [major_triad.inversion(0)]
    )