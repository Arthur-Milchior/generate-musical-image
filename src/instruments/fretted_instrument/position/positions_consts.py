from math import pow

# This should be the only value needed to change in order to scale the whole image.
RATIO_IMAGE = 0.25
"""Global scale factor applied to every other size constant in this module; the single knob to resize the whole
fretboard diagram."""


HEIGHT_OF_FIRST_FRET = 380 * RATIO_IMAGE
"""The height (svg units) of the first fret's cell, before `RATIO_FRET_HEIGHT` shrinks subsequent frets."""
DISTANCE_BETWEEN_STRING = 97 * RATIO_IMAGE
"""The horizontal spacing (svg units) between two adjacent strings."""

MARGIN = DISTANCE_BETWEEN_STRING/2
"""The blank border (svg units) left around the fretboard drawing."""
FRET_THICKNESS = 7* RATIO_IMAGE
"""The stroke width (svg units) of an ordinary fret line."""
TOP_FRET_THICKNESS = round(FRET_THICKNESS*1.4)
"""The stroke width (svg units) of the nut/top fret line, drawn thicker than ordinary frets."""


STRING_THICKNESS = 5 * RATIO_IMAGE
"""The stroke width (svg units) of a string line."""
STROKE_WIDTH = 10 * RATIO_IMAGE
"""The stroke width (svg units) used for note markers (circles/crosses)."""
"""
The ration by which each fret height is reduced.

Fret.make(i+1, a).height() = Fret.make(i, a).height() * RATIO_FRET_HEIGHT"""
RATIO_FRET_HEIGHT = 1/pow(2, 1/12)


"""Ensuring that two nearby circle have a little separation"""
CIRCLE_RADIUS = DISTANCE_BETWEEN_STRING * .47
CIRCLE_STROKE_WIDTH = 5 * RATIO_IMAGE
"""The stroke width (svg units) of a note marker's circle outline."""

FONT_SIZE =12
"""The font size (svg units) used for text labels (e.g. open/not-played markers) on the diagram."""

"""Below-right offset (relative to CIRCLE_RADIUS) and font size ratio (relative to the main text size) for the small finger-number label."""
FINGER_LABEL_OFFSET_RATIO = 1
FINGER_LABEL_FONT_SIZE_RATIO = 0.9