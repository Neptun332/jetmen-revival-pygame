from abc import ABC, abstractmethod
from typing import Tuple, Optional

from Directions import Directions


class Tile(ABC):
    def __init__(
            self,
            color: Tuple[int, int, int],
            x: int,
            y: int,
            world: 'World',
            density: int
    ):
        self.color = color
        self.x = x
        self.y = y
        self.world = world
        self.density = density
        self.active = True

    @abstractmethod
    def is_movable(self):
        ...

    def is_denser_than(self, other_tile: Optional['Tile']) -> bool:
        if other_tile:
            return self.density > other_tile.density
        else:
            return True

    def deactivate(self):
        self.wake_up_neighbours()
        self.active = False

    def wake_up_neighbours(self):
        for direction in Directions:
            neighbour_position = self.get_next_position(direction, 1)
            if not self.world.is_position_inside_scene(*neighbour_position):
                continue
            tile = self.world.get_tile_at_position(
                x=self.x + direction.value[0],
                y=self.y + + direction.value[1]
            )
            if tile and tile.is_movable():
                tile.wake_up_tile()

    def get_next_position(self, direction: Directions, velocity: int) -> Tuple[int, int]:
        return direction.value[0] * velocity + self.x, direction.value[1] * velocity + self.y
