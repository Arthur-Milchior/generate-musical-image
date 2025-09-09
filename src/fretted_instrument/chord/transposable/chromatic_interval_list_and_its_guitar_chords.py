
from dataclasses import dataclass
from fretted_instrument.chord.chromatic_list_and_its_guitar_chords import ChromaticListAndItsGuitarChords
from solfege.value.interval.chromatic_interval import ChromaticInterval
from utils.util import img_tag


@dataclass(frozen=True, unsafe_hash=True)
class ChromaticIntervalListAndItsGuitarChords(ChromaticListAndItsGuitarChords[ChromaticInterval]):
    def chord_pattern_name(self):
        return self.interval_and_its_inversions.easiest_name()

    def alternative_chord_pattern_names(self):
        return self.interval_and_its_inversions.alternative_names()
    
    def csv_content(self):
        l = []
        l.append(self.chord_pattern_name())
        l.append(self.alternative_chord_pattern_names())
        maximals = self.maximals()
        for guitar_chord in maximals:
            l.append(img_tag(guitar_chord.file_name(stroke_colored=False, absolute=False)))
            l.append(img_tag(guitar_chord.file_name(stroke_colored=True, absolute=False)))
        for _ in range(7- len(maximals)):
            l.append("")
            l.append("")
        return l