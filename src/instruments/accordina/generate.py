"""Runs the accordina generators in order: scales, then intervals, then fingerings (importing each submodule
for its side effects — each writes its own SVGs/CSV as it's imported). See `generate/README.md` for details
on each script, and `../../README.md`/`__main__.py` for how this is invoked."""
import instruments.accordina.generate.generate_accordina_scales
import instruments.accordina.generate.generate_accordina_intervals
import instruments.accordina.generate.generate_accordina_fingerings