from accordina.accordina_note import *
from solfege.pattern.scale.scale_pattern import major_scale
from accordina.set_of_accordina_notes import SetOfAccordinaNote
from lily.svg import display_svg_file
from solfege.pattern.scale.scale_pattern import scale_patterns_I_practice
from consts import generate_root_folder
from solfege.value.interval.interval import Interval
from utils.util import ensure_folder, img_tag, save_file
from solfege.value.interval.interval_pattern import IntervalPattern, intervals_up_to_octave

accordina_folder = f"{generate_root_folder}/accordina"
ensure_folder(accordina_folder)

# Generating intervals

interval_folder = f"{accordina_folder}/intervals"
ensure_folder(interval_folder)
anki_interval_notes = []
for interval in intervals_up_to_octave + [IntervalPattern("two octave", Interval.make(chromatic=24, diatonic=14))]:
    interval_name = interval.first_of_the_names(True)
    anki_note =[img_tag("accordina.png"), interval_name]
    for low_note in [AccordinaNote(0), AccordinaNote(1), AccordinaNote(2),]:
        notes = interval.from_note(low_note)
        set = SetOfAccordinaNote(notes)
        svg = set.svg()
        file_name = f"""accordina_{interval_name}_position_{low_note.value}.svg"""
        path = f"{interval_folder}/{file_name}"
        save_file(path, svg)
        anki_note.append(img_tag(file_name))
    anki_interval_notes.append(",".join(anki_note))
anki_file_path = f"""{accordina_folder}/accordina_intervals.csv"""
save_file(anki_file_path, "\n".join(anki_interval_notes))

# generating scales and arpeggios

scales_folder = f"{accordina_folder}/scales"
ensure_folder(scales_folder)
anki_scale_notes = []
for pattern in scale_patterns_I_practice:
    pattern_name = pattern.first_of_the_names(True)
    anki_note =[img_tag("accordina.png"), pattern_name]
    for number_of_octave in [1, 2]:
        for low_note in [AccordinaNote(0), AccordinaNote(1), AccordinaNote(2),]:
            scale = pattern.from_note(low_note, number_of_octaves=number_of_octave)
            notes = scale.notes
            set = SetOfAccordinaNote(notes)
            svg = set.svg()
            file_name = f"""accordina_{pattern_name}_position_{low_note.value}_{"one_octave" if number_of_octave == 1 else "two_octaves"}.svg"""
            path = f"{scales_folder}/{file_name}"
            save_file(path, svg)
            anki_note.append(img_tag(file_name))
    anki_scale_notes.append(",".join(anki_note))
anki_file_path = f"""{accordina_folder}/accordina_scale.csv"""
save_file(anki_file_path, "\n".join(anki_scale_notes))

# Generating fingerings


notes_folder = f"{accordina_folder}/notes"
ensure_folder(notes_folder)
anki_fingering_notes = []
for value in range(accordina_lowest_note.value, accordina_highest_note.value+1):
    fingered_note = AccordinaNote(value, absolute=True)
    set = SetOfAccordinaNote({fingered_note}, absolute= True, min=min_accordina_note, max=max_accordina_note)
    svg_name = f"accordina_{value}.svg"
    svg = set.svg()
    path = f"{notes_folder}/{svg_name}"
    degree = fingered_note.get_degree()
    alteration = "♭" if "♭" in degree else ("#" if "#" in degree else "")
    save_file(path, svg)
    anki_fingering = [
        "Accordina",
        degree,#degree
        alteration, #alteration
        str(fingered_note.octave(scientific_notation=True)), #octave
        "", # function
        img_tag(file_name)
        ]
    anki_fingering_notes.append(",".join(anki_fingering))

anki_file_path = f"""{accordina_folder}/accordina_fingering.csv"""
save_file(anki_file_path, "\n".join(anki_fingering_notes))