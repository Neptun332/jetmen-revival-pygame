from abc import ABC
from typing import Tuple


class Tile(ABC):
    def __init__(
            self,
            color: Tuple[int, int, int],
            x: int,
            y: int
    ):
        self.color = color
        self.x = x
        self.y = y
