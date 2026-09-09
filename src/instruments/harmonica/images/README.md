This folder holds only static, pre-rendered `.svg` assets (one per hole/blow-draw combination, `blow1.svg`
through `blow10.svg` and `draw1.svg` through `draw10.svg`) — there is no Python here, nothing to document as
code. As noted in [`../README.md`](../README.md), running the current generator (`python3 -m
instruments.harmonica` from `src/`) does **not** actually update these files (a relative-path bug makes it
write into `src/harmonica/images/` instead), so treat the contents here as a possibly-stale snapshot rather
than guaranteed-fresh output.
