
from typing import List
from solfege.pattern.chord.chord_patterns import chord_patterns
from solfege.value.interval.role.interval_role_from_string import role_from_interval_index
from solfege.value.key.keys import *
from solfege.pattern.scale.scale_pattern import ScalePattern



pentatonic_major = ScalePattern.make_relative(
    names=["Pentatonic major", "Six-nine arpeggio", "6/9 arpeggio"],
    relative_intervals=[2, 2, (3, 2), 2, (3, 2)], interval_for_signature=nor_flat_nor_sharp,
    source=["https://en.wikipedia.org/wiki/Pentatonic_scale", "https://en.wikipedia.org/wiki/Added_tone_chord"],
    description="A five-note 'gapped' version of the major scale using degrees 1, 2, 3, 5 and 6 (omitting 4 and "
                 "7). It can also be built by taking five consecutive pitches from the "
                 "<a href=\"https://en.wikipedia.org/wiki/Circle_of_fifths\">circle of fifths</a> and "
                 "folding them into one octave, and "
                 "<a href=\"https://en.wikipedia.org/wiki/Pentatonic_scale\">pentatonic scales</a> of this shape "
                 "arose independently in many of the world's musical cultures. Its five pitch classes are "
                 "identical to those of the "
                 "<a href=\"https://en.wikipedia.org/wiki/Added_tone_chord#6/9_chord\">six-nine chord</a> "
                 "arpeggiated, so that arpeggio is not modelled as a separate scale pattern (see "
                 "multi_octave_patterns.md).")
major_scale = ScalePattern.make_relative(
    names=["Major", "Greek Lydian tonos (diatonic genus)"], relative_intervals=[2, 2, 1, 2, 2, 2, 1],
    interval_for_signature=nor_flat_nor_sharp,
    source=["https://en.wikipedia.org/wiki/Major_scale", "https://en.wikipedia.org/wiki/Ionian_mode"],
    description="The <a href=\"https://en.wikipedia.org/wiki/Major_scale\">major</a> "
                 "(<a href=\"https://en.wikipedia.org/wiki/Ionian_mode\">Ionian</a>) scale is the archetypal "
                 "Western diatonic scale, with step pattern whole-whole-half-whole-whole-whole-half. Ancient "
                 "Greek theory assigned this exact interval pattern to the diatonic genus of the Lydian tonos, a "
                 "name later reassigned to a different scale (the modern Lydian mode, below) once Greek tonos "
                 "names were carried into medieval church-mode theory in reverse order.")
pentatonic_minor = ScalePattern.make_relative(
    names=["Pentatonic minor"], relative_intervals=[(3, 2), 2, 2, (3, 2), 2],
    interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Pentatonic_scale",
    description="A five-note scale derived from the natural minor scale by dropping its 2nd and 6th degrees, "
                 "leaving root, ♭3, 4, 5 and ♭7. It is the backbone scale of "
                 "<a href=\"https://en.wikipedia.org/wiki/Blues\">blues</a>, rock and Appalachian folk "
                 "music because none of its intervals clash strongly with either major or minor harmony — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Pentatonic_scale\">Pentatonic scale</a>.")
minor_natural = ScalePattern.make_relative(
    names=["Minor natural", "Aeolian mode"], relative_intervals=[2, 1, 2, 2, 1, 2, 2],
    interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Aeolian_mode",
    description="Better known as the natural minor scale, the "
                 "<a href=\"https://en.wikipedia.org/wiki/Aeolian_mode\">Aeolian mode</a> was one of four modes "
                 "added to the medieval eight-mode system by Swiss humanist Heinrich Glarean in his 1547 "
                 "treatise Dodecachordon, corresponding to the white-key octave from A to A. It is the unaltered "
                 "basis from which the harmonic and melodic minor scales below are formed.")
blues = ScalePattern.make_relative(
    names=["Blues"], relative_intervals=[(3, 2), 2, (1, 0, "BN"), 1, (3, 2), 2], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Blues_scale",
    description="Typically the minor pentatonic scale plus an added chromatic ♭5 'blue note' between the 4th "
                 "and 5th degrees. The blue note reflects the "
                 "<a href=\"https://en.wikipedia.org/wiki/Blues\">blues</a> practice of bending or singing "
                 "pitches microtonally rather than striking them squarely, and the "
                 "<a href=\"https://en.wikipedia.org/wiki/Blues_scale\">scale</a> is central to blues, jazz and "
                 "rock improvisation.")
minor_harmonic = ScalePattern.make_relative(
    names=["Minor harmonic"], relative_intervals=[2, 1, 2, 2, 1, 3, 1], interval_for_signature=three_flats,
    source="https://en.wikipedia.org/wiki/Harmonic_minor_scale",
    description="Raises the natural minor's 7th degree by a semitone so it acts as a "
                 "<a href=\"https://en.wikipedia.org/wiki/Leading-tone\">leading tone</a> into the tonic, at the "
                 "cost of an unusual augmented second between the 6th and 7th degrees. It answers the practical "
                 "need, in tonal harmony, for a minor key to still support a major (dominant) V chord — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Harmonic_minor_scale\">Harmonic minor scale</a>.")
chromatic_scale_pattern = ScalePattern.make_relative(names=["Chromatic"], relative_intervals=
                                                 [(1, 0), (1, 1), (1, 0), (1, 1), (1, 1), (1, 0), (1, 1), (1, 0),
                                                  (1, 1), (1, 0), (1, 1),
                                                  (1, 1), ], interval_for_signature=nor_flat_nor_sharp, role_maker=role_from_interval_index,
    source="https://en.wikipedia.org/wiki/Chromatic_scale",
    description="Contains all twelve <a href=\"https://en.wikipedia.org/wiki/Equal_temperament\">"
                 "equal-tempered</a> pitches a semitone apart, making it the 'total' scale from which every "
                 "other Western scale is a subset. Its name comes from the Greek chroma ('color'); it became a "
                 "self-standing compositional resource with "
                 "<a href=\"https://en.wikipedia.org/wiki/Arnold_Schoenberg\">Schoenberg</a>'s early-20th-century "
                 "atonal and twelve-tone methods — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Chromatic_scale\">Chromatic scale</a>.")
minor_melodic = ScalePattern.make_relative(
    names=["Minor melodic"], relative_intervals=[2, 1, 2, 2, 2, 2, 1], interval_for_signature=three_flats, _descending=minor_natural,
    source=["https://en.wikipedia.org/wiki/Minor_scale", "https://en.wikipedia.org/wiki/Jazz_minor_scale"],
    description="Raises the natural minor's 6th and 7th degrees by a semitone when ascending, smoothing over the "
                 "harmonic minor's awkward augmented second, and classically reverts to the plain natural minor "
                 "when descending — see <a href=\"https://en.wikipedia.org/wiki/Minor_scale\">Minor scale</a>. In "
                 "jazz theory the ascending form is used in both directions and is often called the "
                 "<a href=\"https://en.wikipedia.org/wiki/Jazz_minor_scale\">jazz minor scale</a>.")

# A few added-tone/sixth chords happen to arpeggiate to the exact same pitch-class collection as an existing
# scale (e.g. the six-nine chord arpeggiated is a major pentatonic scale). The scale record keeper forbids
# registering two ScalePatterns with identical intervals (see multi_octave_patterns.md), so for those we don't
# auto-generate a duplicate arpeggio scale here; instead the alternate name is listed directly on the pre-existing
# scale above.
_chords_without_auto_arpeggio = {"Six-nine chord"}
chord_patterns_as_scales = [chord_pattern.to_arpeggio_pattern() for chord_pattern in chord_patterns
                             if chord_pattern.first_of_the_names() not in _chords_without_auto_arpeggio]
scale_patterns_I_practice: List[ScalePattern] = [pentatonic_major, major_scale, pentatonic_minor, minor_natural, blues, minor_harmonic, chromatic_scale_pattern,  minor_melodic] + chord_patterns_as_scales

whole_tone = ScalePattern.make_relative(
    names=["Whole tone"], relative_intervals=[(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2)], interval_for_signature=one_sharp, role_maker=role_from_interval_index,
    source="https://en.wikipedia.org/wiki/Whole-tone_scale",
    description="Built entirely from whole-step intervals, giving six equally spaced, symmetric notes per octave "
                 "with no leading tone and no strong sense of tonic. Its blurred, floating quality made it a "
                 "favorite device of "
                 "<a href=\"https://en.wikipedia.org/wiki/Claude_Debussy\">Claude Debussy</a> and other "
                 "composers escaping traditional tonal function — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Whole-tone_scale\">Whole-tone scale</a>.")
# Petrushka chord, see https://en.wikipedia.org/wiki/Petrushka_chord . Two major triads a tritone apart
# (C major and F# major); collapsed to one octave it is a six-note collection, hence a ScalePattern rather than
# a ChordPattern (see multi_octave_patterns.md).
petrushka_chord = ScalePattern.make_relative(
    names=["Petrushka chord"], relative_intervals=[(1, 1), (3, 2), (2, 1), (1, 1), (3, 1), (2, 1)],
    interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Petrushka_chord",
    description="<a href=\"https://en.wikipedia.org/wiki/Igor_Stravinsky\">Stravinsky</a>'s C major and F♯ "
                 "major triads sounded together (from the second tableau of the ballet "
                 "<a href=\"https://en.wikipedia.org/wiki/Petrushka_(ballet)\">Petrushka</a>), representing the "
                 "puppet's two clashing, mocking faces. The two triads are a "
                 "<a href=\"https://en.wikipedia.org/wiki/Tritone\">tritone</a> apart, the maximally dissonant "
                 "relationship in twelve-tone "
                 "<a href=\"https://en.wikipedia.org/wiki/Equal_temperament\">equal temperament</a>, which "
                 "prevents either triad's key from winning out over the other. Collapsed to one octave, as "
                 "stored here, the six pitch classes form a symmetric "
                 "<a href=\"https://en.wikipedia.org/wiki/Hexatonic_scale\">hexatonic</a> collection — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Petrushka_chord\">Petrushka chord</a>.")
# Elektra chord, see https://en.wikipedia.org/wiki/Elektra_chord . A polychord of E major and C#/Db major a
# tritone apart; collapsed to one octave it has 5 distinct pitch classes, hence a ScalePattern (see
# multi_octave_patterns.md).
elektra_chord = ScalePattern.make_relative(
    names=["Elektra chord"], relative_intervals=[(3, 2), (1, 0), (3, 2), (3, 2), (2, 1)],
    interval_for_signature=nor_flat_nor_sharp,
    source="https://en.wikipedia.org/wiki/Elektra_chord",
    description="<a href=\"https://en.wikipedia.org/wiki/Richard_Strauss\">Richard Strauss</a>'s signature "
                 "chord for the title character of his opera "
                 "<a href=\"https://en.wikipedia.org/wiki/Elektra_(opera)\">Elektra</a> (1909): a bitonal "
                 "polychord combining E major and C♯ (enharmonically D♭) major, two triads a "
                 "<a href=\"https://en.wikipedia.org/wiki/Tritone\">tritone</a> apart, played together. "
                 "Collapsed to one octave, as stored here, its five distinct pitch classes form the underlying "
                 "scale; the complex, unresolved dissonance of the two superimposed keys is exactly what makes "
                 "the chord instantly recognisable as Elektra's musical signature — see "
                 "<a href=\"https://en.wikipedia.org/wiki/Elektra_chord\">Elektra chord</a>.")
scale_patterns = scale_patterns_I_practice + [whole_tone, petrushka_chord, elektra_chord,
    ScalePattern.make_relative(
        names=["Greek Dorian tonos (chromatic genus)"], relative_intervals=[1, 1, 3, 2, 1, 1, 3],
        interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Genus_(music)",
        description="In ancient Greek theory, each tonos (here Dorian) could be tuned in one of three "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">genera</a> depending on the two "
                     "movable notes inside its "
                     "<a href=\"https://en.wikipedia.org/wiki/Tetrachord\">tetrachords</a>. The chromatic genus "
                     "compresses the tetrachord's lower interval into two adjacent semitones (a 'pyknon') below "
                     "a remaining augmented second, producing a denser sound than the diatonic genus below."),
    ScalePattern.make_relative(
        names=["Acoustic", "overtone", "lydian dominant", "Lydian ♭7"], relative_intervals=[2, 2, 2, 1, 2, 1, 2], interval_for_signature=one_sharp,
        source="https://en.wikipedia.org/wiki/Acoustic_scale",
        description="The Lydian mode (below) with a flattened 7th degree (1-2-3-♯4-5-6-♭7); it is the fourth "
                     "mode of the ascending melodic minor scale above. It is called "
                     "<a href=\"https://en.wikipedia.org/wiki/Acoustic_scale\">'acoustic' or 'overtone'</a> "
                     "because its notes closely approximate the 8th through 14th partials of the natural "
                     "harmonic series."),
    ScalePattern.make_relative(
        names=["Altered", "Super-Locrian", "Locrian flat four", "Pomeroy", "Ravel", "diminished whole tone"],
        relative_intervals=[1, 2, 1, 2, 2, 2, 2], interval_for_signature=seven_sharps,
        source="https://en.wikipedia.org/wiki/Altered_scale",
        description="The seventh mode of the ascending melodic minor scale; it "
                     "<a href=\"https://en.wikipedia.org/wiki/Altered_scale\">alters</a> every non-essential "
                     "tone against a dominant seventh chord, making it a staple for high-tension jazz "
                     "improvisation over altered dominants. It differs from the ordinary Locrian mode (below) "
                     "only by a lowered rather than natural 4th degree; the alternate name 'diminished whole "
                     "tone' reflects that its lower tetrachord resembles the half-whole diminished scale and "
                     "its upper tetrachord resembles the whole-tone scale above."),
    ScalePattern.make_relative(
        names=["Augmented", ], relative_intervals=[(3, 2), (1, 0), (3, 2), (1, 0), (3, 2), 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Hexatonic_scale",
        description="A six-note symmetric scale of alternating minor thirds and semitones, equivalent to "
                     "interlocking two augmented triads a minor third apart (hence 'augmented scale') — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Hexatonic_scale\">Hexatonic scale</a>. As a "
                     "genuinely symmetric scale it only became compositionally practical once instruments were "
                     "tuned in twelve-tone "
                     "<a href=\"https://en.wikipedia.org/wiki/Equal_temperament\">equal temperament</a>, and it "
                     "appears notably in "
                     "<a href=\"https://en.wikipedia.org/wiki/Franz_Liszt\">Liszt</a>'s Faust Symphony."),
    ScalePattern.make_relative(
        names=["Prometheus", "Mystic chord"], relative_intervals=[2, 2, 2, (3, 2), 1, 2],
        interval_for_signature=nor_flat_nor_sharp,  # one flat one sharp, can't decide
        source="https://en.wikipedia.org/wiki/Mystic_chord",
        description="The six-note collapsed pitch-class scale derived from "
                     "<a href=\"https://en.wikipedia.org/wiki/Alexander_Scriabin\">Alexander Scriabin</a>'s "
                     "<a href=\"https://en.wikipedia.org/wiki/Mystic_chord\">'mystic chord'</a> "
                     "(C-F♯-B♭-E-A-D, often analysed as stacked fourths), which he used as the harmonic and "
                     "melodic basis of his late works, above all the 1910 tone poem Prometheus: The Poem of "
                     "Fire. Scriabin considered the chord a mystical, unifying sonority and called it his "
                     "'synthetic harmony'; the name 'mystic chord' itself was only coined in 1916. As stored "
                     "here the chord's original spread voicing (spanning more than two octaves) is folded into "
                     "one octave — see multi_octave_patterns.md."),
    ScalePattern.make_relative(
        names=["Tritone", ], relative_intervals=[1, 3, (2, 2), (1, 0), (3, 2), 2], interval_for_signature=one_flat,
        source="https://en.wikipedia.org/wiki/Jazz_scale",
        description="No dedicated Wikipedia article exists for this scale; the general "
                     "<a href=\"https://en.wikipedia.org/wiki/Jazz_scale\">Jazz scale</a> article is used as the "
                     "closest approximation. The tritone scale is a synthetic, symmetric six-note scale built "
                     "from two major triads a "
                     "<a href=\"https://en.wikipedia.org/wiki/Tritone\">tritone</a> apart (e.g. "
                     "C-D♭-E-F♯-G-B♭), used over dominant chords to bring out altered tensions such as ♭9 and "
                     "♯11."),
    ScalePattern.make_relative(
        names=["Bebop dominant", ], relative_intervals=[2, 2, 1, 2, 2, 1, (1, 0), 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="The best-known <a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">bebop scale</a>, "
                     "formed by adding a chromatic passing tone between the ♭7 and root of the Mixolydian mode "
                     "(below), giving eight notes so chord tones consistently fall on strong beats. Jazz "
                     "educator David Baker coined the term 'bebop scales' for this family, associating it with "
                     "players like "
                     "<a href=\"https://en.wikipedia.org/wiki/Charlie_Parker\">Charlie Parker</a>, Dizzy "
                     "Gillespie and Bud Powell.")
    ,
    ScalePattern.make_relative(
        names=["Bebop dorian", "Bebop minor"], relative_intervals=[2, 1, (1, 0), 1, 2, 2, 1, 2, ], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="Formed by adding a chromatic passing tone between the ♭3 and 4th of the Dorian mode "
                     "(below), keeping the same eight-note, on-beat chord-tone alignment as the other "
                     "<a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">bebop scales</a>. Since it shares "
                     "its pitch content with the dominant bebop scale built a fourth below, it is often played "
                     "over ii-chords in ii-V-I progressions."),
    ScalePattern.make_relative(
        names=["Alternate bebop dorian"], relative_intervals=[2, 1, 2, 2, 2, 1, (1, 0), 1, ], interval_for_signature=two_flats,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="No separately named Wikipedia treatment exists for this specific variant; used here as an "
                     "approximation via the general "
                     "<a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">Bebop scale</a> article. It "
                     "represents an alternative placement of the added chromatic passing tone within the "
                     "Dorian-derived bebop scale above."),
    ScalePattern.make_relative(
        names=["Bebop major", ], relative_intervals=[2, 2, 1, 2, (1, 0), 1, 2, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="Built from the major (Ionian) scale above by inserting a chromatic passing tone (♯5) "
                     "between the 5th and 6th degrees, again yielding an eight-note "
                     "<a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">bebop scale</a> that keeps chord "
                     "tones (1, 3, 5, 6) on the beat. It is commonly used over major and major-sixth chords."),
    ScalePattern.make_relative(
        names=["Bebop melodic minor", ], relative_intervals=[2, 1, 2, 2, (1, 0), 1, 2, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="Derived from the ascending melodic minor scale above by adding a chromatic passing tone "
                     "between the 5th and 6th degrees — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">Bebop scale</a>. It is typically "
                     "played over minor-sixth or minor-major-seventh chords."),
    ScalePattern.make_relative(names=["Bebop harmonic minor", "Bebop natural minor"], relative_intervals=[2, 1, 2, 2, 1, 2, (1, 0), 1],
                           interval_for_signature=three_flats,
        source="https://en.wikipedia.org/wiki/Bebop_scale",
        description="Derived from the harmonic minor scale above by adding a passing ♭7 between the ♭6 and the "
                     "leading tone. Because it contains tones usable across all three chords of a minor ii-V-i "
                     "progression, it is a versatile choice for minor-key "
                     "<a href=\"https://en.wikipedia.org/wiki/Bebop_scale\">bebop</a> lines."),
    ScalePattern.make_relative(names=["Double harmonic major", "Byzantine", "Arabic", "Gypsi major"], relative_intervals=[1, 3, 1, 2, 1, 3, 1],
                           interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Double_harmonic_scale",
        description="The major scale above with a flattened 2nd and 6th degree (1-♭2-3-4-5-♭6-7), producing two "
                     "augmented seconds that bracket the tonic and give it a distinctive 'Eastern' color; it is "
                     "called '"
                     "<a href=\"https://en.wikipedia.org/wiki/Double_harmonic_scale\">double harmonic</a>' "
                     "because it contains two harmonic-minor-like tetrachords. It is enharmonically equivalent "
                     "to the Byzantine scale, the Arabic maqam Hijaz Kar, and the Indian raga "
                     "Bhairav/Mayamalavagowla."),
    ScalePattern.make_relative(
        names=["Enigmatic"], relative_intervals=[1, 3, 2, 2, 2, 1, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Enigmatic_scale",
        description="Invented by Bologna Conservatory professor Adolfo Crescentini and popularized after "
                     "Milan's Gazzetta musicale challenged readers to harmonize it in 1888, this ascending "
                     "<a href=\"https://en.wikipedia.org/wiki/Enigmatic_scale\">scale</a> (C-D♭-E-F♯-G♯-A♯-B-C) "
                     "mixes elements of major, minor and whole-tone scales. "
                     "<a href=\"https://en.wikipedia.org/wiki/Giuseppe_Verdi\">Giuseppe Verdi</a>'s own solution "
                     "to the challenge became his 'Ave Maria (sulla scala enigmatica)', part of the Quattro "
                     "Pezzi Sacri (1898)."),
    ScalePattern.make_relative(
        names=["Descending Enigmatic"], relative_intervals=[1, 3, 1, 3, 2, 1, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Enigmatic_scale",
        description="<a href=\"https://en.wikipedia.org/wiki/Giuseppe_Verdi\">Verdi</a> specified a distinct "
                     "descending form of the "
                     "<a href=\"https://en.wikipedia.org/wiki/Enigmatic_scale\">scala enigmatica</a>, different "
                     "from a simple retrograde of the ascending version above, for use in his 'Ave Maria (sulla "
                     "scala enigmatica)'. It shares the ascending enigmatic scale's unusual mix of wide and "
                     "narrow steps but with a different interval ordering."),
    # ScalePattern.make_relative(names=["Flamenco mode"], relative_intervals=[1, 3, 1, 2, 1, 3, 1], unison) can't find anymore on wp
    # (article does in fact exist at https://en.wikipedia.org/wiki/Flamenco_mode; left commented out/unrecovered
    # since the exact interval pattern used above could not be re-confirmed against it)
    ScalePattern.make_relative(names=["Hungarian", "Hungarian Gypsy"], relative_intervals=[2, 1, 3, 1, 1, 2, 2], interval_for_signature=three_flats,
        source="https://en.wikipedia.org/wiki/Gypsy_scale",
        description="The natural minor scale above with a raised (sharpened) 4th degree, giving "
                     "1-2-♭3-♯4-5-♭6-♭7. It is one of several scales collectively called '"
                     "<a href=\"https://en.wikipedia.org/wiki/Gypsy_scale\">Gypsy scales</a>' for their "
                     "association with Romani musical traditions, distinct from the harmonic-minor-based "
                     "Hungarian minor scale below."),
    ScalePattern.make_relative(names=["Half diminished"], relative_intervals=[2, 1, 2, 1, 2, 2, 2], interval_for_signature=five_flats,
        source="https://en.wikipedia.org/wiki/Half_diminished_scale",
        description="Also called Locrian natural-2 or Aeolian ♭5, this is the sixth mode of the ascending "
                     "melodic minor scale above, differing from the ordinary Locrian mode (below) by having a "
                     "natural rather than flattened 2nd degree. Its "
                     "<a href=\"https://en.wikipedia.org/wiki/Half_diminished_scale\">name</a> avoids confusion "
                     "with the (unrelated) diminished scale, and it is the standard scale choice over "
                     "half-diminished (m7♭5) chords.")
    ,
    ScalePattern.make_relative(names=["Harmonic major"], relative_intervals=[2, 2, 1, 2, 1, 3, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Harmonic_major_scale",
        description="The major scale above with a lowered 6th degree (1-2-3-4-5-♭6-7), sharing its upper "
                     "tetrachord with the harmonic minor scale above. Introduced by theorist Moritz Hauptmann "
                     "in the 1850s and later named by Rimsky-Korsakov, who considered it one of the four scales "
                     "forming the '"
                     "<a href=\"https://en.wikipedia.org/wiki/Harmonic_major_scale\">basis of harmony</a>'."),
    ScalePattern.make_relative(names=["Hirajōshi Burrows"], relative_intervals=[(4, 2), 2, 1, (4, 2), 1], interval_for_signature=one_sharp,
        source="https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale",
        description="One of several documented interval readings of the "
                     "<a href=\"https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale\">hirajoshi scale</a> — a "
                     "hemitonic pentatonic tuning adapted from shamisen music by Yatsuhashi Kengyo for the "
                     "<a href=\"https://en.wikipedia.org/wiki/Koto_(instrument)\">koto</a> — this version, "
                     "attributed to theorist Burrows, uses the interval sequence 4-2-1-4-1 semitones (e.g. "
                     "C-E-F♯-G-B)."),
    ScalePattern.make_relative(names=["Hirajōshi Kostka and Payne-Speed"], relative_intervals=[2, 1, (4, 2), 1, (4, 2)],
                           interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale",
        description="Another documented rotation of the "
                     "<a href=\"https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale\">hirajoshi scale</a>, "
                     "attributed to theorists Kostka & Payne and to Speed, using the interval sequence "
                     "2-1-4-1-4 semitones (e.g. C-D-E♭-G-A♭); this reading coincides with the third mode of the "
                     "related in scale below."),
    ScalePattern.make_relative(names=["Hungarian minor"], relative_intervals=[2, 1, 3, 1, 1, 3, 1], interval_for_signature=three_flats,  # should also have one sharp
        source="https://en.wikipedia.org/wiki/Hungarian_minor_scale",
        description="Also called the double harmonic minor or Gypsy minor scale, this is the harmonic minor "
                     "scale above with a raised 4th degree (1-2-♭3-♯4-5-♭6-7). It is prominent in Hungarian "
                     "Romani music and in classical works by "
                     "<a href=\"https://en.wikipedia.org/wiki/Franz_Liszt\">Liszt</a> and Kodaly — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Hungarian_minor_scale\">Hungarian minor scale</a>."),
    ScalePattern.make_relative(names=["Greek Dorian tonos (diatonic genus)", "Phrygian mode"], relative_intervals=[1, 2, 2, 2, 1, 2, 2],
                           interval_for_signature=three_flats,
        source="https://en.wikipedia.org/wiki/Phrygian_mode",
        description="The modern <a href=\"https://en.wikipedia.org/wiki/Phrygian_mode\">Phrygian mode</a> is "
                     "the natural minor scale above with a lowered 2nd degree, named after the ancient kingdom "
                     "of Phrygia. Its interval pattern happens to match the diatonic genus of the ancient Greek "
                     "Dorian tonos — an example of how tonos names were reassigned when carried into medieval "
                     "church-mode theory, so the ancient 'Dorian' label does not correspond to the modern "
                     "Dorian mode (below)."),
    ScalePattern.make_relative(names=["Miyako-bushi"], relative_intervals=[1, (4, 2), 2, 1, (4, 2)], interval_for_signature=two_flats,
        source="https://en.wikipedia.org/wiki/In_scale",
        description="An older name for the <a href=\"https://en.wikipedia.org/wiki/In_scale\">in scale</a>, a "
                     "pentatonic tuning adapted from shamisen music by Yatsuhashi Kengyo for the "
                     "<a href=\"https://en.wikipedia.org/wiki/Koto_(instrument)\">koto</a> (1-♭2-4-♭5-♭7 "
                     "pattern). In traditional Japanese scale theory it represents the more refined counterpart "
                     "to the rustic-sounding yo scale below."),
    ScalePattern.make_relative(names=["Insen"], relative_intervals=[1, (4, 2), 2, (3, 2), 2], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Insen_scale",
        description="A koto/shamisen tuning scale closely related to the hirajoshi scale above, differing from "
                     "it by only one note (e.g. D-E♭-G-A-C) — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Insen_scale\">Insen scale</a>. It corresponds to "
                     "the ragas Revati and Bairagi Bhairav in Indian Carnatic and Hindustani music respectively."),
    ScalePattern.make_relative(names=["Iwato", "Hirajōshi Sachs-Slonimsky"], relative_intervals=[1, (4, 2), 1, (4, 2), 2], interval_for_signature=five_flats,
        source=["https://en.wikipedia.org/wiki/Iwato_scale", "https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale"],
        description="A pentatonic koto scale resembling the Locrian mode (below) with its 3rd and 6th omitted "
                     "(1-♭2-4-♭5-♭7), used in traditional Japanese music and considered a mode of the "
                     "<a href=\"https://en.wikipedia.org/wiki/Hiraj%C5%8Dshi_scale\">hirajoshi scale</a> above — "
                     "see <a href=\"https://en.wikipedia.org/wiki/Iwato_scale\">Iwato scale</a>. It bears the "
                     "intervals (1-4-1-4-2 semitones) that theorists Sachs and Slonimsky separately gave for "
                     "the hirajoshi scale, hence the shared naming."),
    ScalePattern.make_relative(names=["Lydian augmented"], relative_intervals=[2, 2, 2, 2, 1, 2, 1], interval_for_signature=three_sharps,
        source="https://en.wikipedia.org/wiki/Lydian_augmented_scale",
        description="The third mode of the ascending melodic minor scale above, equivalent to a major scale "
                     "with both a raised 4th and raised 5th degree (1-2-3-♯4-♯5-6-7) — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Lydian_augmented_scale\">Lydian augmented "
                     "scale</a>. It combines the brightness of the Lydian mode (below) with the tension of an "
                     "augmented triad on the tonic."),
    ScalePattern.make_relative(names=["Major Locrian"], relative_intervals=[2, 2, 1, 1, 2, 2, 2], interval_for_signature=five_flats,
        source="https://en.wikipedia.org/wiki/Major_Locrian_scale",
        description="Also called <a href=\"https://en.wikipedia.org/wiki/Major_Locrian_scale\">Locrian "
                     "major</a> or Aeolian Dominant ♭5, this scale sharpens the 2nd and 3rd degrees of the "
                     "ordinary Locrian mode (below) while retaining its diminished 5th."),
    ScalePattern.make_relative(names=["Minyo"], relative_intervals=[(3, 2), 2, (3, 2), 2, 2], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Min%27y%C5%8D",
        description="The min'yo scale is an anhemitonic pentatonic scale associated with Japanese folk song "
                     "(<a href=\"https://en.wikipedia.org/wiki/Min%27y%C5%8D\">min'yo</a>), built from 'nuclear "
                     "tones' a fourth apart with an intervening tone, giving the ascending interval sequence "
                     "2-3-2-2-3 semitones. No dedicated 'min'yo scale' article exists separately, so the "
                     "general Min'yo (folk-song genre) article is used as the closest match."),
    ScalePattern.make_relative(names=["Neapolitan minor"], relative_intervals=[1, 2, 2, 2, 1, 3, 1], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Neapolitan_scale",
        description="One of two <a href=\"https://en.wikipedia.org/wiki/Neapolitan_scale\">Neapolitan "
                     "scales</a> (with Neapolitan major, below), formed from the harmonic minor scale above but "
                     "with a lowered 2nd degree, giving 1-♭2-♭3-4-5-♭6-7. It shares the Phrygian mode's "
                     "characteristic minor 2nd above the tonic and is associated with Naples-linked "
                     "18th-century opera composers such as Domenico Scarlatti and Cimarosa. Compare the "
                     "similarly-named "
                     "<a href=\"https://en.wikipedia.org/wiki/Neapolitan_chord\">Neapolitan chord</a> — a "
                     "harmony rather than a scale, see chord/chord_patterns.py's major triad."),
    ScalePattern.make_relative(names=["Neapolitan major"], relative_intervals=[1, 2, 2, 2, 2, 2, 1], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Neapolitan_scale",
        description="The counterpart to the Neapolitan minor above, distinguished by a major (rather than "
                     "minor) 6th degree, giving 1-♭2-♭3-4-5-6-7 — effectively a melodic minor scale with a "
                     "flattened 2nd — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Neapolitan_scale\">Neapolitan scale</a>. Like the "
                     "minor form, it takes its name from the Naples opera tradition of the 18th century.")
    ,
    ScalePattern.make_relative(names=["Pelog"], relative_intervals=[1, 2, 3, 1, 1, 2, 2, ], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Pelog",
        description="One of the two essential tuning systems of Indonesian "
                     "<a href=\"https://en.wikipedia.org/wiki/Gamelan\">gamelan</a> (alongside slendro, below), "
                     "<a href=\"https://en.wikipedia.org/wiki/Pelog\">pelog</a> is a seven-note scale with "
                     "unequal, non-tempered steps. Most gamelan ensembles only use five of its seven pitches at "
                     "a time, grouped into regional modes (pathet), such as the 'bem' and 'barang' subsets "
                     "below."),
    ScalePattern.make_relative(names=["Pelog bem"], relative_intervals=[1, (5, 2), 1, 1, (4, 2)], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Pelog",
        description="A five-note subset (pathet) of the seven-tone "
                     "<a href=\"https://en.wikipedia.org/wiki/Pelog\">pelog</a> scale above, using pitches 1, "
                     "2, 3, 5 and 6 — the tuning used on gamelan gender instruments built for the 'bem'/nem-lima "
                     "modal grouping."),
    ScalePattern.make_relative(names=["Pelog barang"], relative_intervals=[2, (4, 2), 1, 2, (3, 2)], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Pelog",
        description="The complementary five-note subset (pathet) of the "
                     "<a href=\"https://en.wikipedia.org/wiki/Pelog\">pelog</a> scale above, using pitches 2, "
                     "3, 5, 6 and 7 in place of pitch 1 — the tuning used on gender instruments built for the "
                     "'barang' modal grouping."),
    ScalePattern.make_relative(names=["Persian"], relative_intervals=[1, 3, 1, 1, 2, 3, 1], interval_for_signature=five_flats,
        source="https://en.wikipedia.org/wiki/Persian_scale",
        description="A seven-note scale (1-♭2-3-4-♭5-♭6-7) featuring frequent half steps and augmented "
                     "seconds, sometimes described as the Locrian mode (below) with a major 3rd and major 7th "
                     "— see <a href=\"https://en.wikipedia.org/wiki/Persian_scale\">Persian scale</a>. It "
                     "corresponds to the Hindustani raga Lalit."),
    ScalePattern.make_relative(names=["Phrygian dominant"], relative_intervals=[1, 3, 1, 2, 1, 2, 2], interval_for_signature=four_flats,
        source="https://en.wikipedia.org/wiki/Phrygian_dominant_scale",
        description="The fifth mode of the harmonic minor scale above, resembling the Phrygian mode above but "
                     "with a major rather than minor 3rd (1-♭2-3-4-5-♭6-♭7). Also known as the Hijaz or "
                     "freygish scale, it is central to Arabic, Eastern European, Central Asian, flamenco, and "
                     "Jewish <a href=\"https://en.wikipedia.org/wiki/Klezmer\">klezmer</a>/liturgical music — "
                     "see <a href=\"https://en.wikipedia.org/wiki/Phrygian_dominant_scale\">Phrygian dominant "
                     "scale</a>."),
    ScalePattern.make_relative(names=["Greek Phrygian tonos (chromatic genus)"], relative_intervals=[3, 1, 1, 2, 3, 1, 1],
                           interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Genus_(music)",
        description="The chromatic-genus tuning of the ancient Greek Phrygian "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">tonos</a>, in which the "
                     "<a href=\"https://en.wikipedia.org/wiki/Tetrachord\">tetrachord</a>'s two movable notes "
                     "compress its lower interval into two adjacent semitones below a remaining augmented "
                     "second — the same chromatic-genus principle applied to a different named tonos than the "
                     "Dorian and Lydian entries elsewhere in this scale set."),
    ScalePattern.make_relative(names=["Slendro", "Yo descending"], relative_intervals=[2, (3, 2), 2, 2, (3, 2)], interval_for_signature=nor_flat_nor_sharp,
        source=["https://en.wikipedia.org/wiki/Slendro", "https://en.wikipedia.org/wiki/Yo_scale"],
        description="<a href=\"https://en.wikipedia.org/wiki/Slendro\">Slendro</a> is the anhemitonic five-note "
                     "<a href=\"https://en.wikipedia.org/wiki/Gamelan\">gamelan</a> tuning system (the other "
                     "being pelog above), dividing the octave into roughly equidistant steps that vary from "
                     "region to region. Its near-equal-step, no-semitone shape closely resembles the Japanese "
                     "<a href=\"https://en.wikipedia.org/wiki/Yo_scale\">yo scale</a> played in descending "
                     "(rotated) form, hence the shared listing."),
    ScalePattern.make_relative(names=["Two-semitone tritone"], relative_intervals=[1, (1, 0), (4, 2), 1, 1, (4, 2)], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Two-semitone_tritone_scale",
        description="A symmetric six-note scale built from a repeating pattern of two semitones followed by a "
                     "major third (e.g. C-D♭-D-F♯-G-A♭), usable as a substitute for any mode of the melodic "
                     "minor scale above in jazz improvisation. It "
                     "<a href=\"https://en.wikipedia.org/wiki/Two-semitone_tritone_scale\">originates</a> in "
                     "Nicolas Slonimsky's Thesaurus of Scales and Melodic Patterns."),
    ScalePattern.make_relative(names=["Misheberak", "Ukrainian Dorian"], relative_intervals=[2, 1, 3, 1, 2, 1, 2], interval_for_signature=two_flats,  # shold also have one sharp
        source="https://en.wikipedia.org/wiki/Ukrainian_Dorian_scale",
        description="Also called the Dorian ♯4 scale, this raises the 4th degree of the Dorian mode (below), "
                     "giving a "
                     "<a href=\"https://en.wikipedia.org/wiki/Ukrainian_Dorian_scale\">scale</a> long common in "
                     "Jewish, Greek, Ukrainian and Romanian music. The term 'Ukrainian Dorian' was coined by "
                     "musicologist Abraham Zevi Idelsohn after Ukrainian folklorist Filaret Kolessa; in Jewish "
                     "liturgical music it is called the Mi Sheberakh or Misheberak mode."),
    ScalePattern.make_relative(names=["Yo ascending"], relative_intervals=[2, (3, 2), 2, (3, 2), 2], interval_for_signature=two_flats,
        source="https://en.wikipedia.org/wiki/Yo_scale",
        description="A bright-sounding anhemitonic pentatonic scale used in Japanese gagaku, shomyo, and folk "
                     "song, with ascending interval pattern 2-3-2-2-3 semitones (e.g. D-E-G-A-B) — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Yo_scale\">Yo scale</a>. It resembles a gapped "
                     "Dorian mode (below) and is traditionally contrasted with the darker-sounding in scale "
                     "above."),
    ScalePattern.make_relative(names=["Dorian", "Yo with auxiliary", "Greek Phrygian tonos (diatonic genus)"], relative_intervals=[2, 1, 2, 2, 2, 1, 2], interval_for_signature=two_flats,
        source="https://en.wikipedia.org/wiki/Dorian_mode",
        description="The modern <a href=\"https://en.wikipedia.org/wiki/Dorian_mode\">Dorian mode</a> is a "
                     "minor-type diatonic scale corresponding to the white keys D to D. This interval pattern "
                     "coincides with the diatonic genus of the ancient Greek Phrygian "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">tonos</a> — again reflecting the "
                     "historical reshuffling of Greek tonos names in medieval theory — and 'Yo with auxiliary' "
                     "denotes the Japanese "
                     "<a href=\"https://en.wikipedia.org/wiki/Yo_scale\">yo pentatonic scale</a> above filled in "
                     "with extra passing tones to approximate the same seven-note shape."),
    ScalePattern.make_relative(names=["Locrian", "Greek Mixolydian tonos (diatonic genus)"], relative_intervals=[1, 2, 2, 1, 2, 2, 2], interval_for_signature=five_flats,
        source="https://en.wikipedia.org/wiki/Locrian_mode",
        description="The <a href=\"https://en.wikipedia.org/wiki/Locrian_mode\">Locrian mode</a> is the "
                     "seventh mode of the diatonic scale, with a diminished 5th, starting on B using only white "
                     "keys. This pattern matches the diatonic genus of the ancient Greek Mixolydian "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">tonos</a>, another instance of "
                     "the naming mismatch between ancient Greek tonoi and the medieval/modern modes that "
                     "inherited their names."),
    ScalePattern.make_relative(names=["Lydian"], relative_intervals=[2, 2, 2, 1, 2, 2, 1], interval_for_signature=one_sharp,
        source="https://en.wikipedia.org/wiki/Lydian_mode",
        description="The fourth mode of the major scale above, distinguished from the ordinary major scale by "
                     "its raised 4th degree — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Lydian_mode\">Lydian mode</a>. Named after the "
                     "ancient kingdom of Lydia in Anatolia, though it does not correspond intervallically to "
                     "the ancient Greek Lydian tonos (see 'Major' above)."),
    ScalePattern.make_relative(names=["Greek Lydian tonos (chromatic genus)"], relative_intervals=[1, 3, 1, 1, 3, 2, 1],
                           interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Genus_(music)",
        description="The chromatic-genus tuning of the ancient Greek Lydian "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">tonos</a>, compressing the lower "
                     "part of each <a href=\"https://en.wikipedia.org/wiki/Tetrachord\">tetrachord</a> into two "
                     "adjacent semitones below a remaining augmented second, in contrast to the more evenly "
                     "spaced diatonic genus of the same tonos (see 'Major' above)."),
    ScalePattern.make_relative(names=["Mixolydian", "Adonai malakh mode"], relative_intervals=[2, 2, 1, 2, 2, 1, 2], interval_for_signature=one_flat,
        source=["https://en.wikipedia.org/wiki/Mixolydian_mode", "https://en.wikipedia.org/wiki/Adonai_malakh_mode"],
        description="The fifth mode of the major scale above, with a lowered 7th degree, corresponding to the "
                     "white keys G to G — see "
                     "<a href=\"https://en.wikipedia.org/wiki/Mixolydian_mode\">Mixolydian mode</a>. In "
                     "Ashkenazi Jewish liturgical music this same scale is called the "
                     "<a href=\"https://en.wikipedia.org/wiki/Adonai_malakh_mode\">Adonai malakh</a> ('God "
                     "reigns') mode, one of the principal nusach prayer modes."),
    ScalePattern.make_relative(names=["Greek Mixolydian tonos (chromatic genus)"], relative_intervals=[1, (1,0), (3, 2), 1, 1, 3,  2],
                           interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Genus_(music)",
        description="The chromatic-genus tuning of the ancient Greek Mixolydian "
                     "<a href=\"https://en.wikipedia.org/wiki/Genus_(music)\">tonos</a>, following the same "
                     "chromatic-genus principle applied to the Mixolydian tonos rather than the Dorian, "
                     "Phrygian, or Lydian tonoi listed elsewhere in this scale set."),
    ScalePattern.make_relative(names=["Octave"], relative_intervals=[(12, 7)], interval_for_signature=nor_flat_nor_sharp,
        source="https://en.wikipedia.org/wiki/Octave",
        description="The interval between a note and another at twice (or half) its frequency; notes an "
                     "<a href=\"https://en.wikipedia.org/wiki/Octave\">octave</a> apart share the same pitch "
                     "class and are treated as functionally the same note in Western notation.")
]


# Ignored=[
#     "Bohlen-Pierce",
#     "alpha",
#     "Beta",
#     "Delta",
#     "Gamma",
#     "Istrian",
#      "Pfluke",
#     "Non-Pythagorean",
# ]
# (["Algerian"],
#  [2,1,3,1,1,3,1,1, 2,1,2,2,1,3,1,1]),
# (["Greek Dorian tonos (enharmonic genus)"],[0,1,4,2,0,1,4]),
# (["Greek Lydian tonos (enharmonic genus)"],[1,]),
# (["Medieval Lydian mode"],[2,2,2,1,0,2,2,1]),
# (["Greek Mixolydian tonos (enharmonic genus)"],[1,0,1,4,]),
# (["Vietnamese scale of harmonics"],[3,0,1,1,2,5]),
# (["Octatonic"],[2,1,2,1,2,1,2,1]),
# (["Greek Phrygian tonos (enharmonic genus)"],[4,1,0, 2, 4,1,0]),
# (["Medieval Phrygian mode"],[2,2,2,1,0,1,2,2]),
# (["Hypophrygian mode"],[2,2,1,2,0,1,2]),
# (["Harmonic"],0,0,[3,1,1,2,2,3]),
