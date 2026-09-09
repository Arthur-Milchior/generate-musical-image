"""Entry point for `python3 -m instruments.piano`: runs every piano sub-generator (chord progressions, scale
variants, scales, fingering generation, chord successions) by importing each submodule's `main`, which triggers
its generation loop as a side effect of the import (see each submodule's own `main.py`)."""
from instruments.piano.progression import main
from instruments.piano.scale_variant import main
from instruments.piano.scales import main
from instruments.piano.fingering_generation import main
from instruments.piano.chord_successions import main


