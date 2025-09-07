from dataclasses import dataclass

from guitar.position.guitar_position import GuitarPosition

@dataclass(frozen=True)
class Finger:
    index: int
    name: str
    delta: FretDelta

thumb = Finger(0, "thumb")
index = Finger(1, "index")
middle = Finger(2, "middle")
ring = Finger(3, "ring")
little = Finger(4, "little")

@dataclass(frozen=True)
class GuitarPositionWithFinger(GuitarPosition):
    finger: Finger