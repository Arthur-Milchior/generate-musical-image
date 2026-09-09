"""Legacy `unittest`-based runner (see `utils.util.tests_modules`): runs every `unittest.TestCase` found in
`chord_progression`, `generate` and `pattern`. All three modules are currently entirely commented out, so this
has no effect; mostly superseded by `pytest` (see `src/README.md`)."""
from instruments.piano.progression import chord_progression, generate, pattern
from utils.util import tests_modules

tests_modules([chord_progression, generate, pattern])