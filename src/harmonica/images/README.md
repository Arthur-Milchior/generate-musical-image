# harmonica/images

Static assets only — no code. 20 pre-rendered SVG diagrams (`blow1.svg`..`blow10.svg`,
`draw1.svg`..`draw10.svg`), one per harmonica hole x blow/draw combination.

This is where [`../../instruments/harmonica/__init__.py`](../../instruments/harmonica/__init__.py)'s
`drawHarmonica()` actually writes its output when the generator is run the documented way (`cd src &&
python3 -m instruments.harmonica`): the code's relative output path `"harmonica/images/%s%d.svg"` resolves
against the process's current working directory (`src/`), landing here rather than in
[`../../instruments/harmonica/images/`](../../instruments/harmonica/images/) (see that package's own README
for the full explanation of this quirk).

**Duplicate check:** compared by content (md5sum) against
[`../../instruments/harmonica/images/`](../../instruments/harmonica/images/) — the 20 files in both folders are
byte-for-byte identical. This folder is the one actually kept up to date by the generator; the copy under
`instruments/harmonica/images/` is a stale snapshot from whenever it was last regenerated with `cwd` pointed
there instead.
