from solfege.interval import interval, set_of_intervals, \
    too_big_alterations_exception
from solfege.interval import interval_mode
from solfege.interval import abstract_interval, chromatic_interval, diatonic_interval
from utils.util import tests_modules

tests_modules([abstract_interval, chromatic_interval, diatonic_interval, interval, interval_mode, set_of_intervals, too_big_alterations_exception])
