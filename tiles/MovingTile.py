import abc
from typing import Tuple, List, Optional

from Directions import Directions
from tiles.TIle import Tile


class MovingTile(Tile):
    NAME: str

    def __init__(
            self,
            color: Tuple[int, int, int],
            x: int,
            y: int,
            world: 'World',
            velocity: int = 5
    ):
        super().__init__(color, x, y)
        self.settle_color = color
        self.world = world
        self.velocity = velocity
        self.position_should_be_updated = True  # False if tile have neighbours preventing it from moving
        self.tile_have_moved = False
        self.active = True

    @abc.abstractmethod
    def update(self):
        ...

    def update_position(self, possible_movement: Tuple[Directions, ...]):
        if self.position_should_be_updated and self.active:
            self.color = (255, 0, 0)
            tile_have_moved = False
            for direction in possible_movement:
                next_positions = self.get_indexes_on_the_way_to_next_position(direction)
                empty_position = self.get_closes_empty_position(next_positions)
                if empty_position:
                    self.wake_up_neighbours()
                    self.move_to_position(empty_position)
                    tile_have_moved = True

                if tile_have_moved:
                    break

            if not tile_have_moved:
                self.sleep_tile()
        else:
            self.color = self.settle_color

    def wake_up_neighbours(self):
        for direction in Directions:
            neighbour_position = self.get_next_position(direction, 1)
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

    def get_closes_empty_position(self, next_positions: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        last_free_position = None
        for position_on_the_way in next_positions:
            if not self.world.is_position_inside_scene(*position_on_the_way):
                break
            tile_in_next_position = self.world.get_tile_at_position(*position_on_the_way)
            if tile_in_next_position:
                break
            last_free_position = position_on_the_way
        return last_free_position

    def get_next_position(self, direction: Directions, velocity: int) -> Tuple[int, int]:
        return direction.value[0] * velocity + self.x, direction.value[1] * velocity + self.y

    def get_indexes_on_the_way_to_next_position(self, direction: Directions) -> List[Tuple[int, int]]:
        return [self.get_next_position(direction, v) for v in range(1, self.velocity)]

    def move_to_position(self, position: Tuple[int, int]):
        self.world.move_tile_from_one_position_to_other(
            start_position=(self.x, self.y),
            end_position=position
        )
        self.x = position[0]
        self.y = position[1]

    def deactivate(self):
        self.wake_up_neighbours()
        self.active = False
