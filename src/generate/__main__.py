"""Entry point for `python3 -m generate` (run from `src/`): importing `generate_note` and `scales` runs their
module-level generation code as a side effect.

Note: `scales` currently has a pre-existing syntax error (see `scales.py`'s module docstring), so this entry
point currently fails; not fixed here (documentation-only pass)."""

from generate import generate_note, scales
