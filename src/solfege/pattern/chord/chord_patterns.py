"""The catalog of concrete `ChordPattern` instances used elsewhere in the app (triads, seventh chords,
added-tone chords, augmented sixth chords, thirteenth chords...). See ../README.md for the mechanics of
`ChordPattern.make(...)` and this folder's conventions (one octave hard limit, `extension_intervals`,
`optional_fifth`, arpeggios). Unlike scales, chords record into a plain list, so two entries here may
legitimately share the exact same interval list under different names (e.g. distinct enharmonic spellings);
there's no registration-level duplicate check to rely on the way there is for `ScalePattern`."""

from solfege.pattern.chord.chord_pattern import ChordPattern
from solfege.value.key.keys import *

#third and seventh minor or major,

major_triad = ChordPattern.make(
    names=["Major triad"], notation="M",
    _full_interval_list=[(4, 2), (7, 4)], interval_for_signature=nor_flat_nor_sharp,
    source=["https://en.wikipedia.org/wiki/Major_chord", "https://en.wikipedia.org/wiki/Neapolitan_chord"],
    description="Root, major third and perfect fifth: the most consonant, structurally basic "
                 "<a href=\"https://en.wikipedia.org/wiki/Major_chord\">Western chord</a>. "
                 "The same shape built on the flattened second scale degree (♭2) and typically played in first "
                 "inversion is called the <a href=\"https://en.wikipedia.org/wiki/Neapolitan_chord\">Neapolitan "
                 "chord</a>, prized since the Baroque era for its poignant, "
                 "\"grief-stricken\" sound when resolving toward the dominant; it is not a separate pattern here "
                 "since its notes are identical to the plain major triad, only the scale degree it is built on differs.")
minor_triad = ChordPattern.make(
    names=["Minor triad"], notation="m",
    _full_interval_list=[(3, 2), (7, 4)], interval_for_signature=three_flats,
    source=["https://en.wikipedia.org/wiki/Minor_chord", "https://en.wikipedia.org/wiki/Psalms_chord"],
    description="Root, minor third and perfect fifth. "
                 "<a href=\"https://en.wikipedia.org/wiki/Igor_Stravinsky\">Stravinsky</a>'s famous opening chord "
                 "of the Symphony of Psalms (the "
                 "<a href=\"https://en.wikipedia.org/wiki/Psalms_chord\">\"Psalms chord\"</a>) is, in pitch-class "
                 "terms, nothing more than this "
                 "<a href=\"https://en.wikipedia.org/wiki/Minor_chord\">E minor triad</a>; what makes "
                 "it distinctive is not its shape but its voicing, with the third doubled across four octaves while "
                 "the root and fifth sit only at the extreme low and high registers — a doubling/register choice "
                 "this engine does not model (see multi_octave_patterns.md), so it is recorded only in this note.")

dominant_seventh_chord = ChordPattern.make(
    names=["Dominant seventh chord", "major minor seventh chord"], notation="<sup>7</sup>",
    _full_interval_list=[(4, 2), (7, 4), (10, 6)], optional_fifth=True,
    interval_for_signature=one_flat,
    source="https://en.wikipedia.org/wiki/Dominant_seventh_chord",
    description="Major triad plus a minor seventh. Built on the fifth scale degree it is the chord that most "
                 "strongly defines tonal harmony's "
                 "<a href=\"https://en.wikipedia.org/wiki/Dominant_seventh_chord\">dominant function</a>, its "
                 "<a href=\"https://en.wikipedia.org/wiki/Tritone\">tritone</a> between the third and seventh "
                 "wanting to resolve inward to the tonic triad.")


major_seventh_chord = ChordPattern.make(
    names=["Major seventh chord"], notation="<sup>Δ</sup>",
    _full_interval_list=[(4, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Major_seventh_chord",
    description="Major triad plus a major seventh (rather than the dominant chord's minor seventh), giving a "
                 "softer, more consonant \"jazzy\" color than the "
                 "<a href=\"https://en.wikipedia.org/wiki/Major_seventh_chord\">dominant seventh</a>; the Δ "
                 "(delta) notation abbreviates \"major\".")
minor_major_seventh_chord = ChordPattern.make(
    names=["Minor major seventh chord"], notation="m<sup>Δ</sup>",
    _full_interval_list=[(3, 2), (7, 4), (11, 6)], optional_fifth=True, interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Minor_major_seventh_chord",
    description="Minor triad plus a major (rather than minor) seventh. It arises naturally as the tonic chord of "
                 "the harmonic and ascending melodic minor scales, and its clash between the minor third and major "
                 "seventh gives it a tense, "
                 "<a href=\"https://en.wikipedia.org/wiki/Minor_major_seventh_chord\">\"film noir\" sound</a> "
                 "often used by <a href=\"https://en.wikipedia.org/wiki/John_Williams\">John Williams</a> and "
                 "other film composers.")
minor_seven = ChordPattern.make(
    names=["Minor seventh chord"], notation="-<sup>7</sup>",
    _full_interval_list=[(3, 2), (7, 4), (10, 6)], optional_fifth=True, interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Minor_seventh_chord",
    description="Minor triad plus a minor seventh. It is the standard "
                 "<a href=\"https://en.wikipedia.org/wiki/Minor_seventh_chord\">ii chord</a> of major-key ii-V-I "
                 "progressions and the i chord of natural-minor progressions.")

# augmentation

augmented_triad = ChordPattern.make(
    names=["Augmented triad"], notation="+",
    _full_interval_list=[(4, 2), (8, 4)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Augmented_triad",
    description="Root, major third and augmented fifth: two stacked major thirds, dividing the octave "
                 "symmetrically into three equal parts (see "
                 "<a href=\"https://en.wikipedia.org/wiki/Equal_temperament\">equal temperament</a>). Because it "
                 "is <a href=\"https://en.wikipedia.org/wiki/Augmented_triad\">symmetric</a>, every inversion of "
                 "an augmented triad is itself another augmented triad.")
diminished_triad = ChordPattern.make(
    names=["Diminished triad"], notation="-",
    _full_interval_list=[(3, 2), (6, 4)], interval_for_signature=five_flats,
    source="https://en.wikipedia.org/wiki/Diminished_triad",
    description="Root, minor third and diminished fifth: two stacked minor thirds. It is the only diatonic triad "
                 "built on the <a href=\"https://en.wikipedia.org/wiki/Leading-tone\">leading tone</a> (in major) "
                 "and on the second degree (in minor), and its "
                 "<a href=\"https://en.wikipedia.org/wiki/Tritone\">tritone</a> gives it an inherently unstable, "
                 "dissonant sound that wants to resolve.")

augmented_major_seventh_chord = ChordPattern.make(
    names=["Augmented major seventh chord"], notation="+<sup>Δ7</sup>",
    _full_interval_list=[(4, 2), (8, 4), (11, 6)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Seventh_chord",
    description="Augmented triad plus a major seventh: a non-tertian-sounding, impressionistic color chord, one of "
                 "several \"altered fifth\" seventh chords cataloged on the general "
                 "<a href=\"https://en.wikipedia.org/wiki/Seventh_chord\">seventh-chord article</a>.")
diminished_major_seventh_chord = ChordPattern.make(
    names=["Diminished major seventh chord"], notation="<sup>oM7</sup>",
    _full_interval_list=[(3, 2), (6, 4), (11, 6)], interval_for_signature=five_flats,
    source="https://en.wikipedia.org/wiki/Seventh_chord",
    description="Diminished triad plus a major (rather than diminished) seventh; it occurs naturally as the tonic "
                 "seventh chord of the harmonic minor and harmonic major scales, and its stark clash between the "
                 "diminished fifth and major seventh makes it one of the rarer, most dissonant "
                 "<a href=\"https://en.wikipedia.org/wiki/Seventh_chord\">seventh-chord types</a>.")
half_diminished_seventh_chord = ChordPattern.make(
    names=["Half-diminished seventh chord", "Half-diminished chord", "Minor seventh flat five"], notation="<sup>ø7</sup>",
    _full_interval_list=[(3, 2), (6, 4), (10, 6)], interval_for_signature=five_flats,
    source=["https://en.wikipedia.org/wiki/Half-diminished_seventh_chord", "https://en.wikipedia.org/wiki/Tristan_chord"],
    description="Diminished triad plus a minor seventh: the "
                 "<a href=\"https://en.wikipedia.org/wiki/Half-diminished_seventh_chord\">viiø7</a> of a major "
                 "key, and the standard iiø7 chord of minor-key ii-V-i progressions. Respelled as F-B-D♯-G♯, "
                 "this exact shape is the famous "
                 "<a href=\"https://en.wikipedia.org/wiki/Tristan_chord\">\"Tristan chord\"</a> that opens "
                 "<a href=\"https://en.wikipedia.org/wiki/Richard_Wagner\">Wagner</a>'s Tristan und Isolde (1865); "
                 "Wagner's own spelling instead describes it with the compound intervals augmented 4th, augmented "
                 "6th and augmented 9th above the bass, but its notes — and their historic ambiguity about which "
                 "key they even belong to, rather than the notes themselves — are what made the chord influential "
                 "in the move away from traditional tonal harmony.")
augmented_seventh_chord = ChordPattern.make(
    names=["Augmented seventh chord", "seventh augmented fifth chord", "seventh sharp five chord"], notation="+<sup>7</sup>",
    _full_interval_list=[(4, 2), (8, 4), (10, 6)], interval_for_signature=one_flat,
    source="https://en.wikipedia.org/wiki/Augmented_seventh_chord",
    description="Major triad with a raised (augmented) fifth plus a minor seventh: a dominant seventh chord with "
                 "its fifth sharpened, common as an "
                 "<a href=\"https://en.wikipedia.org/wiki/Augmented_seventh_chord\">altered dominant</a> in blues "
                 "and jazz (the \"7♯5\" chord).")
dominant_seventh_flat_five_chord = ChordPattern.make(
    names=["Dominant seventh flat five chord"], notation="<sup>7♭5</sup>",
    _full_interval_list=[(4, 2), (6, 4), (10, 6)], interval_for_signature=five_flats,
    source="https://en.wikipedia.org/wiki/Dominant_seventh_flat_five_chord",
    description="Major third, diminished fifth and minor seventh above the root: a "
                 "<a href=\"https://en.wikipedia.org/wiki/Dominant_seventh_flat_five_chord\">dominant seventh "
                 "chord with its fifth flattened</a> instead of sharpened. It is symmetric under "
                 "<a href=\"https://en.wikipedia.org/wiki/Tritone_substitution\">tritone substitution</a> — "
                 "swapping root and ♭5 gives the same four pitch classes — which is exactly why it works so well "
                 "as a substitute dominant a tritone away.")
major_seventh_flat_five_chord = ChordPattern.make(
    names=["Major seventh flat five chord"], notation="M<sup>7♭5</sup>",
    _full_interval_list=[(4, 2), (6, 4), (11, 6)], optional_fifth=False, interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Seventh_chord",
    description="Major third, diminished fifth and major seventh above the root — a major seventh chord with a "
                 "flattened fifth. It is the rarest of the four altered-fifth "
                 "<a href=\"https://en.wikipedia.org/wiki/Seventh_chord\">seventh chords</a> catalogued there, "
                 "and is enharmonically equivalent to a major seventh chord with a raised (♯5) rather than "
                 "lowered fifth.")

# sixth chords and other added-tone chords, see https://en.wikipedia.org/wiki/Sixth_chord and
# https://en.wikipedia.org/wiki/Added_tone_chord . All of these already fit within one octave, no reduction needed.

major_sixth_chord = ChordPattern.make(
    names=["Major sixth chord", "Sixth chord", "Added sixth chord"], notation="6",
    _full_interval_list=[(4, 2), (7, 4), (9, 5)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Sixth_chord",
    description="Major triad plus an added sixth above the root. In modern (post-Baroque) usage this is an "
                 "<a href=\"https://en.wikipedia.org/wiki/Sixth_chord\">\"added tone\" chord</a>, not an "
                 "inversion — confusingly, \"sixth chord\" in Baroque "
                 "<a href=\"https://en.wikipedia.org/wiki/Figured_bass\">figured-bass</a> terminology instead "
                 "meant a triad's first inversion (a third and sixth above the bass); this pattern is the newer, "
                 "added-tone meaning.")
minor_sixth_chord = ChordPattern.make(
    names=["Minor sixth chord"], notation="m6",
    _full_interval_list=[(3, 2), (7, 4), (9, 5)], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Sixth_chord",
    description="Minor triad plus an added major sixth above the root. Its pitch classes are shared with the "
                 "<a href=\"https://en.wikipedia.org/wiki/Half-diminished_seventh_chord\">half-diminished seventh "
                 "chord</a> a minor third above (they are the same four notes reinterpreted), which is part of "
                 "why the added sixth versus seventh reading is often ambiguous in practice.")
added_ninth_chord = ChordPattern.make(
    names=["Added ninth chord", "Add nine chord", "Add2 chord"], notation="add9",
    _full_interval_list=[(2, 1), (4, 2), (7, 4)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Major triad plus a second/ninth above the root, with no seventh present (unlike a true ninth "
                 "chord). <a href=\"https://en.wikipedia.org/wiki/Added_tone_chord\">Wikipedia</a> calls this "
                 "shape \"add2\" when voiced low and \"add9\" when the added note is voiced an octave higher; "
                 "both name the same pitch classes, so a single closest-position pattern covers them (see "
                 "multi_octave_patterns.md).")
minor_added_ninth_chord = ChordPattern.make(
    names=["Minor added ninth chord", "Minor add nine chord", "Minor add2 chord"], notation="m(add9)",
    _full_interval_list=[(2, 1), (3, 2), (7, 4)], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Minor triad plus an added second/ninth above the root, with no seventh present. Like the major "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord\">add9</a>, this is a closest-position "
                 "stand-in for the same chord voiced with the ninth an octave higher.")
added_fourth_chord = ChordPattern.make(
    names=["Added fourth chord", "Add4 chord", "Added eleventh chord"], notation="add11",
    _full_interval_list=[(4, 2), (5, 3), (7, 4)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Major triad plus an added perfect fourth above the root, with no seventh present. When the "
                 "added note is thought of as an eleventh (a fourth plus an octave) instead, the same pitch "
                 "classes are called an "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord\">\"add11\" chord</a>.")
minor_added_fourth_chord = ChordPattern.make(
    names=["Minor added fourth chord", "Minor added eleventh chord"], notation="m(add11)",
    _full_interval_list=[(3, 2), (5, 3), (7, 4)], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Minor triad plus an added perfect fourth above the root, with no seventh present — the minor "
                 "counterpart of the "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord\">added fourth chord</a> above.")
six_nine_chord = ChordPattern.make(
    names=["Six-nine chord", "6/9 chord"], notation="6/9",
    _full_interval_list=[(2, 1), (4, 2), (7, 4), (9, 5)], interval_for_signature=nor_flat_nor_sharp,
    extension_intervals=[(2, 1)],
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Major triad with both an added sixth and an added ninth above the root, i.e. the union of the "
                 "sixth chord and the add9 chord — see the "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord#6/9_chord\">6/9 chord</a> section. It "
                 "is a common, fully consonant substitute for a major or dominant ninth chord that avoids the "
                 "dissonant major seventh/leading tone. The ninth is marked as an extension (see "
                 "multi_octave_patterns.md): a physical voicing (e.g. on guitar) should place it above the "
                 "root, third, fifth and sixth, not between them.")
minor_six_nine_chord = ChordPattern.make(
    names=["Minor six-nine chord", "Minor 6/9 chord"], notation="m6/9",
    _full_interval_list=[(2, 1), (3, 2), (7, 4), (9, 5)], interval_for_signature=three_flats,
    extension_intervals=[(2, 1)],
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Minor triad with both an added sixth and an added ninth above the root — see the "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord#6/9_chord\">6/9 chord</a> section. Its "
                 "major sixth and major ninth against a minor third give it a Dorian-mode flavor, and it is "
                 "frequently used as a consonant, non-dissonant tonic minor chord in jazz. As with the major "
                 "6/9 chord above, the ninth is marked as an extension that a physical voicing should place "
                 "above the rest of the chord.")
mixed_third_chord = ChordPattern.make(
    names=["Mixed third chord", "Split third chord"], notation="(♭3/3)",
    _full_interval_list=[(3, 2), (4, 3), (7, 4)], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Added_tone_chord",
    description="Contains both the minor and major third above the root at once, alongside the fifth — see the "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord#Mixed_third_chord\">mixed third "
                 "chord</a> section (the upper third is spelled here as a diminished fourth rather than a major "
                 "third — the two are enharmonically identical — because computing this chord's inversions "
                 "breaks if two notes share the same scale degree). In practice blues and blues-rock guitarists "
                 "usually separate the two thirds by an octave or more rather than stacking them right next to "
                 "each other as this closest-position pattern does; the clash between them is exactly the "
                 "blue-note effect that gives blues harmony its color.")

# Augmented sixth chords, see https://en.wikipedia.org/wiki/Augmented_sixth_chord . These are built on the
# flattened submediant (♭6) scale degree and, like the added-tone chords above, already fit within one octave.

italian_sixth_chord = ChordPattern.make(
    names=["Italian sixth chord", "Italian augmented sixth chord"], notation="It<sup>+6</sup>",
    _full_interval_list=[(4, 2), (10, 5)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Augmented_sixth_chord",
    description="Bass, major third and augmented sixth above the bass — the only "
                 "<a href=\"https://en.wikipedia.org/wiki/Augmented_sixth_chord#Italian_sixth\">augmented sixth "
                 "chord</a> with just three distinct notes (the tonic is doubled in four-part writing). Built on "
                 "♭6 and normally resolving outward by step to an octave on the dominant, it is enharmonically "
                 "identical to an incomplete "
                 "<a href=\"https://en.wikipedia.org/wiki/Dominant_seventh_chord\">dominant seventh chord</a>, "
                 "but functions very differently: both outer voices resolve outward to the same pitch class "
                 "rather than one voice resolving down as a seventh would.")
french_sixth_chord = ChordPattern.make(
    names=["French sixth chord", "French augmented sixth chord"], notation="Fr<sup>+6</sup>",
    _full_interval_list=[(4, 2), (6, 3), (10, 5)], interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Augmented_sixth_chord",
    description="Like the Italian sixth, but with an added augmented fourth above the bass — see the "
                 "<a href=\"https://en.wikipedia.org/wiki/Augmented_sixth_chord#French_sixth\">French sixth</a> "
                 "section. All four of its notes belong to a single "
                 "<a href=\"https://en.wikipedia.org/wiki/Whole-tone_scale\">whole-tone scale</a>, giving it the "
                 "same wide, tonally ambiguous color that made the whole-tone scale itself attractive to "
                 "<a href=\"https://en.wikipedia.org/wiki/Claude_Debussy\">French Impressionist composers</a> — "
                 "hence the name.")
german_sixth_chord = ChordPattern.make(
    names=["German sixth chord", "German augmented sixth chord"], notation="Ger<sup>+6</sup>",
    _full_interval_list=[(4, 2), (7, 4), (10, 5)], interval_for_signature=one_flat,
    source="https://en.wikipedia.org/wiki/Augmented_sixth_chord",
    description="Like the Italian sixth, but with an added perfect fifth above the bass — see the "
                 "<a href=\"https://en.wikipedia.org/wiki/Augmented_sixth_chord#German_sixth\">German sixth</a> "
                 "section; the resulting four notes are enharmonically identical to a "
                 "<a href=\"https://en.wikipedia.org/wiki/Dominant_seventh_chord\">dominant seventh chord</a>. It "
                 "is the hardest of the three to resolve cleanly to a root-position tonic or dominant triad "
                 "without producing forbidden parallel fifths, which composers work around by passing through a "
                 "<a href=\"https://en.wikipedia.org/wiki/Second_inversion\">cadential six-four chord</a> first; "
                 "it appears often in Beethoven and later in "
                 "<a href=\"https://en.wikipedia.org/wiki/Ragtime\">ragtime</a>.")

# Thirteenth chords, see https://en.wikipedia.org/wiki/Thirteenth_(interval)#Gallery . A thirteenth is a compound
# sixth (an octave plus a sixth); per multi_octave_patterns.md these are stored with the thirteenth reduced to a
# plain sixth, in closest position. Jazz alterations of the thirteenth chord (13♭9, 13♯11, 13♭5, 13sus,
# "add13" versus "13") mostly collapse onto the same pitch classes once the ninth/eleventh are omitted -- which the
# gallery article itself says is the most common practice -- so only the three canonical forms are modelled here.

dominant_thirteenth_chord = ChordPattern.make(
    names=["Dominant thirteenth chord"], notation="<sup>13</sup>",
    _full_interval_list=[(4, 2), (7, 4), (9, 5), (10, 6)], optional_fifth=True, interval_for_signature=one_flat,
    extension_intervals=[(9, 5)],
    source="https://en.wikipedia.org/wiki/Thirteenth_(interval)",
    description="<a href=\"https://en.wikipedia.org/wiki/Dominant_seventh_chord\">Dominant seventh chord</a> "
                 "plus a "
                 "<a href=\"https://en.wikipedia.org/wiki/Thirteenth_(interval)#Gallery\">thirteenth</a>, stored "
                 "here with the thirteenth reduced to the sixth it is enharmonically identical to (an octave "
                 "lower) and marked as an extension (see multi_octave_patterns.md): a physical voicing (e.g. on "
                 "guitar) should place it above the root, third, fifth and seventh, matching how a real "
                 "thirteenth chord is voiced. In practice the ninth and eleventh are usually also present but "
                 "the fifth, ninth and eleventh are the tones most often dropped in performance, since \"root, "
                 "third, seventh and thirteenth are most often included.\"")
major_thirteenth_chord = ChordPattern.make(
    names=["Major thirteenth chord"], notation="<sup>Δ13</sup>",
    _full_interval_list=[(4, 2), (7, 4), (9, 5), (11, 6)], optional_fifth=True, interval_for_signature=nor_flat_nor_sharp,
    extension_intervals=[(9, 5)],
    source="https://en.wikipedia.org/wiki/Thirteenth_(interval)",
    description="<a href=\"https://en.wikipedia.org/wiki/Major_seventh_chord\">Major seventh chord</a> plus a "
                 "<a href=\"https://en.wikipedia.org/wiki/Thirteenth_(interval)#Gallery\">thirteenth</a>, stored "
                 "here with the thirteenth reduced to a sixth and marked as an extension that a physical "
                 "voicing should place above the root, third, fifth and seventh. The eleventh, when added in "
                 "full extended voicings, is conventionally raised (♯11) to avoid the semitone clash it would "
                 "otherwise make against the major third, and for that reason is commonly left out entirely, "
                 "as it is here.")
minor_thirteenth_chord = ChordPattern.make(
    names=["Minor thirteenth chord", "Minor seventh add thirteenth chord"], notation="m<sup>13</sup>",
    _full_interval_list=[(3, 2), (7, 4), (9, 5), (10, 6)], optional_fifth=True, interval_for_signature=three_flats,
    extension_intervals=[(9, 5)],
    source="https://en.wikipedia.org/wiki/Thirteenth_(interval)",
    description="<a href=\"https://en.wikipedia.org/wiki/Minor_seventh_chord\">Minor seventh chord</a> plus a "
                 "<a href=\"https://en.wikipedia.org/wiki/Thirteenth_(interval)#Gallery\">thirteenth</a>, stored "
                 "here with the thirteenth reduced to a sixth and marked as an extension that a physical "
                 "voicing should place above the root, third, fifth and seventh. Jazz notation distinguishes a fuller \"minor "
                 "thirteenth\" (implying the ninth and eleventh are also present) from a leaner \"minor seventh "
                 "add thirteen\" (only the sixth/thirteenth is added on top of the seventh chord); both reduce to "
                 "the same pitch classes once the ninth and eleventh are left out, as they are in this "
                 "closest-position pattern.")

#triad_patterns = []
#fourad_patterns = [dominant_seventh_chord]
"""Patterns with three notes"""
triad_patterns = [major_triad, minor_triad, augmented_triad, diminished_triad]
"""Patterns with four notes"""
fourad_patterns = [minor_major_seventh_chord, augmented_seventh_chord, diminished_major_seventh_chord,
                   half_diminished_seventh_chord, augmented_major_seventh_chord, dominant_seventh_chord,
                   dominant_seventh_flat_five_chord, major_seventh_chord, major_seventh_flat_five_chord, minor_seven]
"""Sixth chords and other added-tone chords (see https://en.wikipedia.org/wiki/Sixth_chord and
https://en.wikipedia.org/wiki/Added_tone_chord)"""
sixth_and_added_tone_patterns = [major_sixth_chord, minor_sixth_chord, added_ninth_chord, minor_added_ninth_chord,
                                  added_fourth_chord, minor_added_fourth_chord, six_nine_chord, minor_six_nine_chord,
                                  mixed_third_chord]
"""Augmented sixth chords (see https://en.wikipedia.org/wiki/Augmented_sixth_chord)"""
augmented_sixth_patterns = [italian_sixth_chord, french_sixth_chord, german_sixth_chord]
"""Thirteenth chords, stored octave-reduced (see multi_octave_patterns.md)"""
thirteenth_patterns = [dominant_thirteenth_chord, major_thirteenth_chord, minor_thirteenth_chord]


"""All patterns"""
chord_patterns = (triad_patterns + fourad_patterns + sixth_and_added_tone_patterns + augmented_sixth_patterns
                   + thirteenth_patterns)
