from math import pow

# This should be the only value needed to change in order to scale the whole image.
RATIO_IMAGE = 0.25


HEIGHT_OF_FIRST_FRET = 380 * RATIO_IMAGE
DISTANCE_BETWEEN_STRING = 87 * RATIO_IMAGE

MARGIN = DISTANCE_BETWEEN_STRING/2
FRET_THICKNESS = 7* RATIO_IMAGE 
TOP_FRET_THICKNESS = FRET_THICKNESS*1.4


STRING_THICKNESS = 5 * RATIO_IMAGE
STROKE_WIDTH = 10 * RATIO_IMAGE
"""
The ration by which each fret height is reduced.

instrument.fret(i+1).height() = instrument.fret(i).height() * RATIO_FRET_HEIGHT"""
RATIO_FRET_HEIGHT = 1/pow(2, 1/12)


"""Ensuring that two nearby circle have a little separation"""
CIRCLE_RADIUS = DISTANCE_BETWEEN_STRING * 3/8


