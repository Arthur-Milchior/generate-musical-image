Generates images for the harmonica. Smaller/less developed than the other instrument packages: there's no
solfege/note model here, just `__init__.py`'s `drawHarmonica()` drawing a fixed 10-hole outline with one hole
highlighted, for every hole x blow/draw combination. Run via `python3 -m instruments.harmonica` from `src/`
(see [`../../README.md`](../../README.md)).

- `__init__.py`: `drawHarmonica()` plus the module-level loop that calls it 20 times (10 holes x blow/draw),
  writing to `<generate_root_folder>/harmonica/images/` (per `consts.generate_root_folder`, i.e.
  `generated/harmonica/images/` at the repo root), matching the convention every other instrument package uses.
- `__main__.py`: entry point, just imports `__init__` for its side effect.
- `images/`: a handful of pre-rendered SVGs checked in as a fallback/example, from before this package wrote
  to `generate_root_folder` — no longer kept up to date by the current code (real output now goes to
  `generated/harmonica/images/` instead). See [`../../../harmonica/README.md`](../../../harmonica/README.md)
  for the identical, equally-stale sibling copy at the repo's top level.
