from .generate import *

class TestScalesGenerate(unittest.TestCase):
    maxDiff = None

    prefix_path = f"{test_folder}/test_generation"
    ensure_folder(prefix_path)
    c_major = [
        Note("C"),
        Note("D"),
        Note("E"),
        Note("F"),
        Note("G"),
        Note("A"),
        Note("B"),
        Note("C5"),
    ]
    d_flat_major = [
        Note("D♭"),
        Note("E♭"),
        Note("F"),
        Note("G♭"),
        Note("A♭"),
        Note("B♭"),
        Note("C5"),
        Note("D5♭"),
    ]
    two_major_half_tone = c_major + list(reversed(d_flat_major))

    def test_generation_two_way(self):
        best_penalty = generate_best_fingering_for_melody(self.two_major_half_tone, for_right_hand=True)
        fingerings = best_penalty.fingerings
        all_fingering = ListPianoLilyable(
            [LiteralPianoLilyable.factory(key=Note("C"), right_hand=fingering, left_hand=None) for fingering in
             fingerings],
            bar_separator="||")
        lily = all_fingering.lily()
        ensure_folder(test_folder)
        file = f"{test_folder}/generate_new_scale_and_half_tone"
        delete_file_if_exists(f"{file}.ly")
        compile_(lily, file, False, extension="pdf")  # ()

    def test_generation_scale(self):
        best_penalty = generate_best_fingering_for_scale(self.c_major, for_right_hand=True)
        fingerings = best_penalty.fingerings
        all_fingering = ListPianoLilyable(
            [LiteralPianoLilyable.factory(key=Note("C"), right_hand=fingering, left_hand=None) for fingering, _ in
             fingerings],
            bar_separator="||")
        lily = all_fingering.lily()
        ensure_folder(test_folder)
        file = f"{test_folder}/generate_new_scale"
        delete_file_if_exists(f"{file}.ly")
        compile_(lily, file, False, extension="pdf")  # ()

    def generation_helper(self, fundamental: Note, scale_pattern: ScalePattern, for_right_hand: bool,
                          expected: Fingering, key: Optional[Note] = None,
                          show: bool = False):
        key = key or fundamental
        scale = scale_pattern.generate(fundamental, 1)
        best_penalty, fingerings = generate_best_fingering_for_scale(scale.notes,
                                                                     for_right_hand=for_right_hand)
        self.assertEquals(len(fingerings), 1)
        piano_notes, fingering = fingerings[0]
        if show:
            # scale = fingering.generate(first_played_note=fundamental, number_of_octaves=2, scale_pattern=scale_pattern)
            lily_code = lilypond_code_for_one_hand(key=key.lily_in_scale(), notes_or_chords=piano_notes,
                                                   for_right_hand=for_right_hand,
                                                   midi=False)
            ly_path = f"{self.prefix_path}.ly"
            svg_path = f"{self.prefix_path}.svg"
            delete_file_if_exists(svg_path)
            delete_file_if_exists(ly_path)
            cmd = compile_(lily_code, file_prefix=self.prefix_path, execute_lily=True, wav=False)
            cmd()

        self.assertEquals(fingering, expected)

    def test_blues_A_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(note=PianoNote("A", finger=5)).
                    add(note=PianoNote("G", finger=4)).
                    add(note=PianoNote("E", finger=1)).
                    add(note=PianoNote("D#", finger=4)).
                    add(note=PianoNote("D", finger=3)).
                    add(note=PianoNote("C", finger=2)).
                    add(note=PianoNote("A3", finger=1)))
        fundamental = Note("A3")
        self.generation_helper(fundamental=fundamental, scale_pattern=blues, for_right_hand=True, expected=expected,
                               show=False, key=Note("c"))

    def test_blues_D_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(note=PianoNote("D5", finger=5)).
                    add(note=PianoNote("C5", finger=4)).
                    add(note=PianoNote("A", finger=1)).
                    add(note=PianoNote("G#", finger=4)).
                    add(note=PianoNote("G", finger=3)).
                    add(note=PianoNote("F", finger=2)).
                    add(note=PianoNote("D", finger=1)))
        fundamental = Note("D")
        self.generation_helper(fundamental=fundamental, scale_pattern=blues, for_right_hand=True, expected=expected,
                               show=True, key=Note("F"))

    def test_pentatonic_major_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(PianoNote("C# ", finger=5)).
                    add(PianoNote("A# ", finger=3)).
                    add(PianoNote("G# ", finger=2)).
                    add(PianoNote("E# ", finger=1)).
                    add(PianoNote("D# ", finger=2)).
                    add(PianoNote("C# ", finger=1)))
        self.generation_helper(fundamental=Note("C#"), scale_pattern=pentatonic_major, for_right_hand=True,
                               expected=expected, show=False)
        # All black note

    def test_minor_seventh_arpeggio_A_right(self):
        expected = (Fingering(for_right_hand=True).
                    add_pinky_side(PianoNote("A ", finger=5)).
                    add(PianoNote("A ", finger=1)).
                    add(PianoNote("C ", finger=2)).
                    add(PianoNote("E ", finger=3)).
                    add(PianoNote("G ", finger=4)))
        self.generation_helper(fundamental=Note("A"), scale_pattern=minor_seven.to_arpeggio_pattern(),
                               for_right_hand=True, expected=expected, show=False)

    def test_minor_seventh_arpeggio_A_left(self):
        expected = (Fingering(for_right_hand=False).
                    add_pinky_side(PianoNote("A ", finger=4)).
                    add(PianoNote("G ", finger=1)).
                    add(PianoNote("E ", finger=2)).
                    add(PianoNote("C ", finger=3)).
                    add(PianoNote("A ", finger=4))
                    )
        self.generation_helper(fundamental=Note("A2"), scale_pattern=minor_seven.to_arpeggio_pattern(),
                               for_right_hand=False, expected=expected, show=False, key=Note("C"))

    def test_minor_melodic_right(self):
        self.generation_helper(Note("C"), minor_melodic, True, TestFingering.right_minor_melodic_fingering, show=False,
                               key=Note("E♭"))

    def test_minor_melodic_left(self):
        self.generation_helper(Note("C"), minor_melodic, False, TestFingering.left_minor_melodic_fingering,
                               key=Note("E♭"))

    def test_augmented_major_seventh_arpeggio_f_left(self):
        expected = (Fingering(for_right_hand=False).
                    add_pinky_side(PianoNote("F2 ", finger=4)).
                    add(PianoNote("A ", finger=3)).
                    add(PianoNote("C# ", finger=2)).
                    add(PianoNote("E ", finger=1)).
                    add(PianoNote("F ", finger=4)))
        self.generation_helper(Note("F2"), scale_pattern=augmented_major_seventh_chord.to_arpeggio_pattern(),
                               for_right_hand=False, show=False, expected=expected)

    def test_blues_c_d(self):
        notes = blues.generate(Note("C")).notes + list(reversed(blues.generate(Note("D♭")).notes))
        compile_(LiteralPianoLilyable.factory(key=Note("c"), right_hand=notes).lily(), f"{self.prefix_path}/c_d_blues",
                 wav=False)()
        right = generate_best_fingering_for_melody(notes, for_right_hand=True)
        left = generate_best_fingering_for_melody(notes, for_right_hand=False)
        print(left)
        print(right)
