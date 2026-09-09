Generates images for the harmonica. Smaller/less developed than the other instrument packages: there's no
solfege/note model here, just `__init__.py`'s `drawHarmonica()` drawing a fixed 10-hole outline with one hole
highlighted, for every hole x blow/draw combination. Run via `python3 -m instruments.harmonica` from `src/`
(see [`../../README.md`](../../README.md)).

- `__init__.py`: `drawHarmonica()` plus the module-level loop that calls it 20 times (10 holes x blow/draw).
- `__main__.py`: entry point, just imports `__init__` for its side effect.
- `images/`: pre-rendered SVG output, checked in as a fallback/example — see the note below, this folder is
  **not** actually kept up to date by the current code.

**Verified bug/gotcha:** `__init__.py` writes to the relative path `"harmonica/images/%s%d.svg"`, resolved
against the process's *current working directory*, not against this package's own location. Since the
documented way to run this (`cd src && python3 -m instruments.harmonica`) sets `cwd` to `src/`, the generator
actually (re)writes files into **`src/harmonica/images/`** — the sibling top-level folder documented in
[`../../../harmonica/README.md`](../../../harmonica/README.md) — not into this package's own `images/`
folder. Confirmed by actually running the generator: `src/harmonica/images/*.svg` mtimes updated, this
folder's did not. So the `images/` folder here is a stale, no-longer-updated copy (all files share one mtime
from whenever it was last populated); `src/harmonica/images/` is the folder the code currently writes to.
