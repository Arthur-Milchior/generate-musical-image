"""Dead/unused module -- not imported anywhere. The commented-out code below shows an earlier, manual way of
registering every chord's arpeggio as a scale; this is now done automatically by
`solfege.pattern.scale.scale_patterns`'s `chord_patterns_as_scales`, which calls
`ChordPattern.to_arpeggio_pattern()` on every entry of `chord_patterns` at import time."""

# from solfege.pattern.chord.chord_patterns import chord_patterns


# for chord in chord_patterns:
#     #This cause arpeggio to be registered
#     chord.to_arpeggio_pattern()
