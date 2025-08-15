from accordina.note import *
from solfege.scale.scale_pattern import major_scale
from accordina.set_of_notes import SetOfAccordinaNote
from lily.svg import display_svg_file
from solfege.scale.scale_pattern import scale_patterns_I_practice
from consts import generate_root_folder
from solfege.interval.interval import Interval
from utils.util import ensure_folder
from solfege.interval.interval_pattern import IntervalPattern, intervals_up_to_octave

accordina_folder = f"{generate_root_folder}/accordina"
ensure_folder(accordina_folder)

# Generating intervals

interval_folder = f"{accordina_folder}/intervals"
ensure_folder(interval_folder)
anki_interval_notes = []
for interval in intervals_up_to_octave + [IntervalPattern("two octave", Interval(chromatic=24, diatonic=14))]:
    interval_name = interval.get_the_first_of_the_name(True)
    anki_note =["""<img src="accordina.png"/>""", interval_name]
    for low_note in [AccordinaNote(0), AccordinaNote(1), AccordinaNote(2),]:
        notes = interval.get_notes(low_note)
        set = SetOfAccordinaNote(notes)
        svg = set.svg()
        file_name = f"""accordina_{interval_name}_position_{low_note.value}.svg"""
        path = f"{interval_folder}/{file_name}"
        with open(path, "w") as f:
            f.write(svg)
        anki_note.append(f"""<img src="{file_name}"/>""")
    anki_interval_notes.append(",".join(anki_note))
anki_file_path = f"""{accordina_folder}/accordina_intervals.csv"""
with open(anki_file_path, "w") as f:
    f.write("\n".join(anki_interval_notes))

# generating scales and arpeggios

scales_folder = f"{accordina_folder}/scales"
ensure_folder(scales_folder)
anki_scale_notes = []
for pattern in scale_patterns_I_practice:
    pattern_name = pattern.get_the_first_of_the_name(True)
    anki_note =["""<img src="accordina.png"/>""", pattern_name]
    for number_of_octave in [1, 2]:
        for low_note in [AccordinaNote(0), AccordinaNote(1), AccordinaNote(2),]:
            scale = pattern.generate(low_note, number_of_octaves=number_of_octave)
            notes = scale.notes
            set = SetOfAccordinaNote(notes)
            svg = set.svg()
            file_name = f"""accordina_{pattern_name}_position_{low_note.value}_{"one_octave" if number_of_octave == 1 else "two_octaves"}.svg"""
            path = f"{scales_folder}/{file_name}"
            with open(path, "w") as f:
                f.write(svg)
            anki_note.append(f"""<img src="{file_name}"/>""")
    anki_scale_notes.append(",".join(anki_note))
anki_file_path = f"""{accordina_folder}/accordina_scale.csv"""
with open(anki_file_path, "w") as f:
    f.write("\n".join(anki_scale_notes))

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
    with open(path, "w") as f:
        f.write(svg)
    anki_fingering = [
        "Accordina",
        degree,#degree
        alteration, #alteration
        str(fingered_note.get_octave(scientificNotation=True)), #octave
        "", # function
        f"""<img src="{svg_name}"/>"""
        ]
    anki_fingering_notes.append(",".join(anki_fingering))

anki_file_path = f"""{accordina_folder}/accordina_fingering.csv"""
with open(anki_file_path, "w") as f:
    f.write("\n".join(anki_fingering_notes))