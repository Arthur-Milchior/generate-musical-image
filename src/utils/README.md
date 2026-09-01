# utils

Generic, domain-agnostic helpers used across the codebase (nothing here knows about music). The two mechanisms
worth understanding before touching [../solfege/pattern/](../solfege/pattern/) are `DataClassWithDefaultArgument`
(this folder) and the `RecordKeeper`/`SingletonContainer` machinery in [recording/](recording/) (see
[recording/README.md](recording/README.md)).

## [`data_class_with_default_argument.py`](data_class_with_default_argument.py): the `.make()` construction protocol

`DataClassWithDefaultArgument` is a frozen-dataclass mixin that separates "how to build a value with sensible
defaults and light coercion from loosely-typed call sites" from the dataclass's actual `__init__`. Subclasses
never get constructed with `SomeClass(...)` directly in application code — always `SomeClass.make(*args, **kwargs)`.
`make()`:

1. calls `_clean_arguments_for_constructor(args, kwargs)` — coerce/validate values already supplied (e.g. turn a
   plain list into a `FrozenList`, a bare string into a singleton, a tuple into an `Interval`);
2. calls `_default_arguments_for_constructor(args, kwargs)` — fill in a dict of defaults for anything not
   supplied;
3. merges the two (explicit values win) and calls the real dataclass `__init__`.

Both methods are meant to be overridden per-class and must call `super()` — see any of
[../solfege/pattern/solfege_pattern.py](../solfege/pattern/solfege_pattern.py),
[../solfege/pattern/chord/chord_pattern.py](../solfege/pattern/chord/chord_pattern.py),
[../solfege/pattern/scale/scale_pattern.py](../solfege/pattern/scale/scale_pattern.py) for the pattern:
`_maybe_arg_to_kwargs(args, kwargs, "field_name", clean_fn)` pulls a field out of positional `args` if present,
applies `clean_fn`, and leaves it alone if the caller didn't pass it (defaults fill the gap later);
`arg_to_kwargs` is the same but the field is *required*.

**Gotcha this convention exists to avoid:** dataclasses still enforce "no non-default field after a default
field" across the whole inheritance chain, computed from where each field was *first* declared, not from
whichever subclass sets a default value for it. Giving a field a real `field(default=...)`/`= value` at the
dataclass level (instead of routing the default through `_default_arguments_for_constructor`) is a trap the
moment any subclass, anywhere, later adds a plain required field — it will fail with a confusing
`TypeError: non-default argument 'x' follows default argument 'y'` pointing at a class that looks unrelated to
your change. [../solfege/pattern/solfege_pattern.py](../solfege/pattern/solfege_pattern.py)'s `_is_chord_pattern`
broke exactly this way once; keep new fields default-free at the dataclass level and give them defaults only
through `_default_arguments_for_constructor`.

## Other files here

- [`frozenlist.py`](frozenlist.py): `FrozenList[T]` (immutable, hashable list; `StrFrozenList`/`IntFrozenList`
  instantiate it) and `MakeableWithSingleArgument`, a protocol for "this type can be built from one
  loosely-typed argument, or passed through unchanged if already an instance" — used pervasively so pattern
  definitions can pass plain tuples/ints/strings instead of constructing value objects by hand.
- [`frozendict.py`](frozendict.py): `FrozenDict`, an immutable dict wrapper, constructible from a dict or
  kwargs.
- [`easyness.py`](easyness.py): `ClassWithEasyness[KeyType]` — one abstract method, `easy_key()`, used to
  sort/rank patterns by difficulty (patterns are learned/practiced in easiest-first order elsewhere in the app).
- [`util.py`](util.py): the `assert_typing` / `assert_optional_typing` / `assert_iterable_typing` family used
  everywhere instead of static typing for runtime invariants (this codebase leans on asserts, not exceptions,
  for internal invariant violations — a failing assert means a bug in the pattern definition, not bad user
  input).
- [`recording/`](recording/): see [recording/README.md](recording/README.md).
- [`svg/`](svg/), [`csv.py`](csv.py), [`constants.py`](constants.py), [`debug_file.py`](debug_file.py):
  unrelated small utilities (SVG helpers, CSV export, a couple of hard-coded local paths, scratch debug notes)
  — no deep mechanics to document.
