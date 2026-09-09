"""Entry point for `python3 -m instruments.piano.fingering_generation`: importing `generate` currently has no
side effect (the fingering-generation pipeline in `generate.py` is exposed as functions, not run at import
time) — see `generate.py`'s `generate_best_fingering_for_scale`/`generate_best_fingering_for_melody`."""
from instruments.piano.fingering_generation import generate
