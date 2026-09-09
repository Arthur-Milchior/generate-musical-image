"""Package marker for `solfege.value.interval.set`: ordered lists of intervals sharing a common
starting note, used as the shape behind chord/scale patterns before they're anchored to a tonic
(`IntervalList` for chromatic+diatonic, `ChromaticIntervalListPattern` for chromatic-only). Eagerly
imports `interval_list` for its module-level registrations."""

import solfege.value.interval.set.interval_list
