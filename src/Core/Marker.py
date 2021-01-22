from dataclasses import dataclass
from enum import Enum


@dataclass
class MARKER(Enum):
    NONE = "None"
    DIAMOND = "d"
    X = "x"
    PLUS = "+"


def StringToMarker(markerString):
    if markerString == "None":
        return MARKER.NONE
    elif markerString == "d":
        return MARKER.DIAMOND
    elif markerString == "x":
        return MARKER.X
    elif markerString == "+":
        return MARKER.PLUS
