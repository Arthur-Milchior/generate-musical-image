from piano import pianonote, scales
from utils.util import tests_modules
import piano.scales.tests
import piano.chord_successions.tests

tests_modules([pianonote, piano.scales.tests, piano.chord_successions.tests])
