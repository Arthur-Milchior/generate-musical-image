from instruments.accordina.accordina_note import AccordinaNote
from instruments.accordina.set_of_accordina_notes import SetOfAccordinaNote
from solfege.value.interval.interval import Interval
from utils.util import img_tag, save_file
from .accordina_constants import *

from solfege.value.interval.interval_pattern import IntervalPattern, intervals_up_to_octave

interval_folder = f"{accordina_folder}/intervals"
ensure_folder(interval_folder)
anki_interval_notes = []

for interval in intervals_up_to_octave + [IntervalPattern("two octave", Interval.make(_chromatic=24, _diatonic=14))]:
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
