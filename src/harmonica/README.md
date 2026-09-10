This is a top-level-under-`src` folder containing only an `images/` directory of pre-rendered harmonica SVGs
(`blow1.svg`..`blow10.svg`, `draw1.svg`..`draw10.svg`) — no Python of its own, and untracked by git.

**History:** [`../instruments/harmonica/__init__.py`](../instruments/harmonica/__init__.py) used to write its
output to the *relative* path `"harmonica/images/%s%d.svg"`, resolved against the process's current working
directory rather than against the package's own location. Since the documented way to run it (`cd src &&
python3 -m instruments.harmonica`, per [`../README.md`](../README.md)) sets `cwd` to `src/`, that resolved to
**this** folder, `src/harmonica/images/`, rather than the package's own `images/` folder — so this folder used
to be the one the generator actually (re)wrote on every run.

That bug is now fixed: the generator writes to `generated/harmonica/images/` (via
`consts.generate_root_folder`), like every other instrument package. This folder is therefore a frozen,
no-longer-written leftover from before the fix — safe to delete if you don't want it kept around; nothing else
references it.
