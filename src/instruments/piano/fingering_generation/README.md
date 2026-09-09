# fingering_generation

Computes good piano fingerings (which finger plays which note) for an arbitrary melody or for a full scale, by
exhaustively searching every legal finger assignment and keeping the one(s) with the lowest penalty. This is
the algorithm; the result is expressed using [`../scales/fingering.py`](../scales/fingering.py)'s `Fingering`
class, and [`../scales/`](../scales/) is this package's main consumer (it needs a fingering for every scale
pattern starting on every note before it can render a score).

## Files

- [`generate.py`](generate.py) — the search itself:
  - `generate_best_fingering` — the recursive core: try every legal next finger for the next note, prune
    branches that are already worse than the best complete fingering found so far, and collect every fingering
    tied for the best final penalty.
  - `generate_best_fingering_for_melody` — thin wrapper for an arbitrary (not necessarily one-octave-scale)
    sequence of notes.
  - `generate_best_fingering_for_scale` — wrapper for a full scale (checks the fingering is one octave, and
    additionally penalizes the wrap-around transition back to the tonic).
  - `BestPenaltyMelody`/`BestPenaltyScale` — the running best-so-far result: a penalty plus every fingering
    achieving it.
- [`penalty_for_scale.py`](penalty_for_scale.py) — `PenaltyForScale`: the scoring/ordering model. Tracks counts
  of each kind of awkward transition (thumb on a black key, thumb-passing that is not diatonically adjacent,
  etc.); one `PenaltyForScale` is always comparable (worse/better) to another via `__gt__`/`__ge__`, in the
  priority order documented on the class.
- [`penalty.py`](penalty.py) — `Penalty`: a `PenaltyForScale` subclass used while a fingering is still being
  built note-by-note and its extremities (hence the extremity-dependent part of the score) aren't known yet; it
  plugs in a neutral `MockFingering` so comparisons stay well-defined in the meantime.
- `main.py`/`__main__.py` — entry point for `python3 -m instruments.piano.fingering_generation`; currently a
  no-op (importing `generate` has no side effect — the module only defines functions, it does not run
  anything), so this package is only ever used as a library by `../scales/`.
- `test_generate.py`/`test_penalty_for` — commented-out (`test_generate.py`) or currently-unrunnable
  (`test_penalty_for`, which is missing its `.py` extension and its `import unittest`/other imports — a
  pre-existing issue, not something introduced here) test files.

## Known issues

`generate.py`'s `generate_best_fingering_for_scale` calls `FingeringSymbol.from_scale(...)`, but no
`FingeringSymbol` is defined or imported anywhere in this package (only `Fingering` is) — this is a
pre-existing bug that makes that function raise `NameError` if actually called; it most likely should read
`Fingering.from_scale`. Left unfixed here since fixing it is a behavior change, not a documentation one.
