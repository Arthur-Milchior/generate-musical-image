from solfege.pattern.inversion.chromatic_intervals_and_its_inversions import ChromaticIntervalListAndItsInversions
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from solfege.pattern.chord.chord_patterns import major_triad

major_chromatic_interval_list_and_its_inversion = ChromaticIntervalListAndItsInversions(
    chromatic_intervals=ChromaticIntervalListPattern.make_absolute([0, 4, 7]),
    inversions = [major_triad.inversion(0)]
    )