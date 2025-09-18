from solfege.value.interval import interval, too_big_alterations_exception
from solfege.value.interval import interval_mode
from solfege.value.interval import abstract_interval, chromatic_interval, diatonic_interval
from utils.util import tests_modules

tests_modules([abstract_interval, chromatic_interval, diatonic_interval, interval, interval_mode, too_big_alterations_exception])
