"""Entry point for `python3 -m instruments.piano.scales`. The second import is meant to ensure arpeggio
patterns are registered from the scale patterns before `main` runs (see
`solfege.pattern.chord.chord_pattern.add_arpeggios_to_scales`, which `main.py`'s `generate.py` already calls at
import time) but currently points at a non-existent module (`solfege.scale.scale_pattern`; the real path is
`solfege.pattern.scale.scale_pattern`) and raises `ModuleNotFoundError` — a pre-existing bug."""
from instruments.piano.scales import main
import solfege.scale.scale_pattern #Ensure that the arpeggios are generated from the scales