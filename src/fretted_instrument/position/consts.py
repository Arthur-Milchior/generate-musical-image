from math import pow

HEIGHT_OF_FIRST_FRET = 380
DISTANCE_BETWEEN_STRING = 87

WIDTH = DISTANCE_BETWEEN_STRING * 6
MARGIN = DISTANCE_BETWEEN_STRING/2


"""
The ration by which each fret height is reduced.

instrument.fret(i+1).height() = instrument.fret(i).height() * RATIO_FRET_HEIGHT"""
RATIO_FRET_HEIGHT = 1/pow(2, 1/12)


"""Ensuring that two nearby circle have a little separation"""
CIRCLE_RADIUS = DISTANCE_BETWEEN_STRING * 3/8