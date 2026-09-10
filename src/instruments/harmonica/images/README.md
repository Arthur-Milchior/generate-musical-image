This folder holds only static, pre-rendered `.svg` assets (one per hole/blow-draw combination, `blow1.svg`
through `blow10.svg` and `draw1.svg` through `draw10.svg`) — there is no Python here, nothing to document as
code. As noted in [`../README.md`](../README.md), the generator now writes to
`generated/harmonica/images/` (per `consts.generate_root_folder`), not here — so treat the contents of this
folder as a fixed, pre-refactor snapshot rather than guaranteed-fresh output.
