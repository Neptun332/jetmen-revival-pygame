from abc import ABC
from typing import Tuple, Optional


class Tile(ABC):
    def __init__(
            self,
            color: Tuple[int, int, int],
            x: int,
            y: int,
            density: int
    ):
        self.color = color
        self.x = x
        self.y = y
        self.density = density

    def is_denser_than(self, other_tile: Optional['Tile']) -> bool:
        if other_tile:
            return self.density > other_tile.density
        else:
            return True
