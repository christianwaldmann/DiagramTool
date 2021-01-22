from dataclasses import dataclass
from enum import Enum


@dataclass
class COLOR(Enum):
    BLACK = "black"
    WHITE = "white"
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    ORANGE = "orange"
    TOMATO = "tomato"


def StringToColor(colorString):
    if colorString == "black":
        return COLOR.BLACK
    elif colorString == "white":
        return COLOR.WHITE
    elif colorString == "blue":
        return COLOR.BLUE
    elif colorString == "red":
        return COLOR.RED
    elif colorString == "green":
        return COLOR.GREEN
    elif colorString == "orange":
        return COLOR.ORANGE
    elif colorString == "tomato":
        return COLOR.TOMATO
