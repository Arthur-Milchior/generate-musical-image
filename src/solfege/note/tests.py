from solfege.interval import abstract_interval
from solfege.note import alteration, note, set_of_notes
from solfege.note import chromatic_note, diatonic_note
from utils.util import tests_modules

tests_modules([abstract_interval, alteration, chromatic_note, diatonic_note, note, set_of_notes])