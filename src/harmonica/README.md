This is a top-level-under-`src` folder containing only an `images/` directory of pre-rendered harmonica SVGs
(`blow1.svg`..`blow10.svg`, `draw1.svg`..`draw10.svg`) — no Python of its own. It looks, at first glance, like
a stale duplicate of [`../instruments/harmonica/images/`](../instruments/harmonica/images/) (same file names,
byte-identical content as of this writing), and the sibling package's own README used to describe it that way
— but that turned out to be backwards.

**What actually happens:** [`../instruments/harmonica/__init__.py`](../instruments/harmonica/__init__.py)
writes its output to the *relative* path `"harmonica/images/%s%d.svg"`, resolved against the process's
current working directory rather than against the package's own location. The documented way to run it
(`cd src && python3 -m instruments.harmonica`, per [`../README.md`](../README.md)) sets `cwd` to `src/`, so
`"harmonica/images/"` resolves to **this** folder, `src/harmonica/images/` — confirmed by actually running the
generator: every file's mtime in this `images/` folder updated, while
`src/instruments/harmonica/images/`'s did not move at all.

So, despite the name/location suggesting `src/harmonica/` is the legacy one: this folder is the one the
current code actually (re)writes on every run, while `src/instruments/harmonica/images/` is the stale,
no-longer-updated copy (all of its files share a single old mtime, consistent with being seeded once and
never touched since). Nothing has been deleted or moved as part of documenting this — see
[`../instruments/harmonica/README.md`](../instruments/harmonica/README.md) for the fix suggestion (the
generator should build its output path from `__file__`/`consts.generate_root_folder` like the other
instruments do, instead of a bare relative string).
