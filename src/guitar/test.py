from .pos import Pos
from solfege.note import ChromaticInterval
from solfege.note import ChromaticNote


empty = Pos(1,0)
assert (repr(empty)=="Pos(1,0)")
assert(empty.svg()=="""
  <circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
assert(empty.getChromatic()==ChromaticNote(-8))

one = Pos(1,1)
assert (repr(one)=="Pos(1,1)")
assert(one.svg()=="""
  <circle cx="15" cy="50" r="11" fill="black" stroke="black" stroke-width="3"/>""")

assert (one.getChromatic() == ChromaticNote(-7))
assert (one-empty == ChromaticInterval(1))
assert (empty-one == ChromaticInterval(-1))
assert (one-one == ChromaticInterval(0))
assert (empty.add(ChromaticInterval(1)) == one)
assert (empty.add(ChromaticInterval(4)) == Pos(1,4))
assert (empty.add(ChromaticInterval(6)) == Pos(2,1))

assert(one.toSop().svg()=="""\
<svg xmlns="http://www.w3.org/2000/svg" width="180" height="100" version="1.1">
  <line x1="15" y1="25" x2="15" y2="75" stroke-width="4" stroke="black" />
  <line x1="45" y1="25" x2="45" y2="75" stroke-width="4" stroke="black" />
  <line x1="75" y1="25" x2="75" y2="75" stroke-width="4" stroke="black" />
  <line x1="105" y1="25" x2="105" y2="75" stroke-width="4" stroke="black" />
  <line x1="135" y1="25" x2="135" y2="75" stroke-width="4" stroke="black" />
  <line x1="165" y1="25" x2="165" y2="75" stroke-width="4" stroke="black" />
  <line x1="15" y1="25" x2="165" y2="25" stroke-width="4" stroke="black" />
  <line x1="15" y1="75" x2="165" y2="75" stroke-width="4" stroke="black" />
  <circle cx="15" cy="50" r="11" fill="black" stroke="black" stroke-width="3"/>
</svg>""")
