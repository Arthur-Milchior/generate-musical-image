# src

This is the actual Python package. Everything under it is pure standard library — the checked-in
`.venv` has no third-party packages installed, `pip install` is not needed. The one external dependency is a
`lilypond` binary on `PATH` (used by [`_lily/lily.py`](_lily/lily.py) to render piano staff notation to SVG);
everything else (fretted-instrument diagrams, saxophone fingering charts, accordina button charts) is drawn with
this repo's own SVG code in [`utils/svg/`](utils/svg/) and needs nothing external.

## Layout

- [`solfege/`](solfege/) — the music-theory model (notes, intervals, keys, and the chord/scale/inversion
  *patterns* — see [`solfege/pattern/README.md`](solfege/pattern/README.md) to start). Nothing here draws
  anything; it only knows about music theory.
- [`instruments/`](instruments/) — one subpackage per instrument (`piano/`, `fretted_instrument/` (guitar/bass/
  ukulele-style fretted instruments), `saxophone/`, `accordina/`, `harmonica/`), each turning
  `solfege` patterns into images and Anki notes for that instrument. See each subfolder's own README.
- [`lily/`](lily/) / [`_lily/`](_lily/) — LilyPond integration (piano/staff notation only).
- [`generate/`](generate/) — a few cross-instrument generation entry points (note tables, scale numbering).
- [`utils/`](utils/) — generic helpers, most importantly the `.make()` construction protocol and the pattern
  record-keeper machinery — see [`utils/README.md`](utils/README.md).
- [`inheritance.md`](inheritance.md) — the base-class ordering convention used across the dataclass hierarchy.
- `test_*` / `*.py` files directly under `src/` (`consts.py`, `sh.py`) are small shared config/shell helpers, not
  a package of their own.

## Running the tests

```sh
cd src
python3 -m pytest solfege   # or any subpackage/file path
```
This repo's `pytest` needs to come from the system install (`/usr/bin/pytest` in this environment) — the local
`.venv` doesn't have it. A handful of pre-existing, unrelated tests are known to fail (some `RecordKeeper`
container-type mismatches, one stale `__repr__` string) — see the commit history around
"interval notation"/"Add source links and descriptions to chord/scale patterns" for the currently-known set.

## Running the generators

```sh
cd src
python3 __main__.py                     # fretted instrument + piano + harmonica, per src/__main__.py
python3 -m instruments.<name>           # a single instrument: accordina, fretted_instrument, harmonica, piano, saxophone
```
Output is written to `../generated` (relative to `src/`, i.e. `generated/` at the repo root — gitignored),
per [`consts.py`](consts.py)'s `generate_root_folder`.

Note: the repository-root `README`/`__main__.py` describe running `python3 .` from the repo root; in this
checkout that resolves to `from main import *` and there is no `main.py`, so that entry point is currently
broken. Use the `src/__main__.py`/`python3 -m instruments.<name>` commands above instead.
