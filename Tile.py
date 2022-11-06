import abc
from abc import ABC
from typing import Tuple

from Directions import Directions


class Tile(ABC):
    NAME: str

    def __init__(
            self,
            color: Tuple[int, int, int],
            x: int,
            y: int,
            world: 'World'
    ):
        # render stuff
        self.color = color
        self.settle_color = color
        # # Physics stuff
        # self.density = density
        # position
        self.x = x
        self.y = y
        self.world = world
        self.position_should_be_updated = True  # False if tile have neighbours preventing it from moving
        self.tile_have_moved = False

    @abc.abstractmethod
    def update(self):
        ...

    def update_position(self, possible_movement: Tuple[Directions, ...]):
        if self.position_should_be_updated:
            self.color = (255, 0, 0)
            tile_have_moved = False
            for direction in possible_movement:
                next_position = self.get_next_position(direction)
                # TODO add density for water
                if not self.world.is_position_inside_scene(*next_position):
                    continue
                tile_in_next_position = self.world.get_tile_at_position(*next_position)
                if not tile_in_next_position:
                    self.wake_up_neighbours()
                    self.move_to_position(next_position)
                    tile_have_moved = True
                    break

            if not tile_have_moved:
                self.sleep_tile()
        else:
            self.color = self.settle_color

    def wake_up_neighbours(self):
        for direction in Directions:
            neighbour_position = self.get_next_position(direction)
            if not self.world.is_position_inside_scene(*neighbour_position):
                continue
            tile = self.world.get_tile_at_position(
                x=self.x + direction.value[0],
                y=self.y + + direction.value[1]
            )
            if tile:
                tile.wake_up_tile()

    def wake_up_tile(self):
        self.position_should_be_updated = True

    def sleep_tile(self):
        self.position_should_be_updated = False

    def get_next_position(self, direction: Directions) -> Tuple[int, int]:
        return self.x + direction.value[0], self.y + direction.value[1]

    def move_to_position(self, position: Tuple[int, int]):
        self.world.move_tile_from_one_position_to_other(
            start_position=(self.x, self.y),
            end_position=position
        )
        self.x = position[0]
        self.y = position[1]
