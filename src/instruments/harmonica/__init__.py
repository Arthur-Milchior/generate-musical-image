from utils.util import *

square = 30


def drawHarmonica(f, pos, draw):
    f.write(
        """<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">""" % (square * 11, square * 3))
    # vertical
    for i in range(0, 11):
        f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="%s" />""" % (
        square * (i + 0.5), square * .5, square * (i + 0.5), square * (1.5), "black"))
    # numbers
    for i in range(1, 11):
        f.write("""<text x="%d" y="%d" fill="%s" font-size="30">%d</text>""" % (
        square * (i - .5), square * (1.3), "black" if i != pos else "red", i))
    # horizontal
    for i in range(1, 3):
        f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="4" stroke="black" />""" % (
        square * .5, square * (i - 0.5), square * 10.5, square * (i - .5)))
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * pos, square * 1.5, square * pos, square * 2.5))
    end_of_arrow = square * 2.5 if draw else square * 1.5
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * (pos + .25), square * 1.75, square * pos, end_of_arrow))
    f.write("""<line x1="%d" y1="%d" x2="%d" y2="%d" stroke-width="2" stroke="red" />""" % (
    square * (pos - .25), square * 1.75, square * pos, end_of_arrow))

    f.write("</svg>")


for draw in [True, False]:
    for pos in range(1, 11):
        ensure_folder("harmonica/images/")
        with open("harmonica/images/%s%d.svg" % ("draw" if draw else "blow", pos), "w") as f:
            drawHarmonica(f, pos, draw)
