"""Package marker for `solfege.value`; eagerly imports the `interval`, `key` and `note` subpackages so
that importing `solfege.value` is enough to make them (and their module-level registrations) available."""

import solfege.value.interval
import solfege.value.key
import solfege.value.note
