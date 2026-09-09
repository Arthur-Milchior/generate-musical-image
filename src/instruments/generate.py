"""Cross-instrument entry point: importing this module runs the accordina, saxophone and fretted-instrument
generators (each module's generation happens at import time as a side effect). `piano` and `harmonica` are
currently commented out here; see each instrument's own `README.md`/`__main__.py` to run it individually via
`python3 -m instruments.<name>`."""
#import instruments.piano.generate
import instruments.accordina.generate
#import instruments.harmonica.generate
import instruments.saxophone.generate
import instruments.fretted_instrument.generate