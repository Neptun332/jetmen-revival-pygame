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
            density: int,
            velocity: int = 5
    ):
        super().__init__(color, x, y, world, density)
        self.settle_color = color
        self.velocity = velocity
        self.position_should_be_updated = True  # False if tile have neighbours preventing it from moving
        self.tile_have_moved = False
        self.active = True

    def is_movable(self):
        return True

    def update_position(self, possible_movement: Tuple[Directions, ...]):
        if self.position_should_be_updated and self.active:
            self.color = (255, 0, 0)
            tile_have_moved = False

            for direction in possible_movement:
                next_positions = self.get_indexes_on_the_way_to_next_position(direction)
                position_that_is_able_to_move = self.get_closes_position_that_is_able_to_move(next_positions)
                if position_that_is_able_to_move:
                    self.swap_position(position_that_is_able_to_move)
                    tile_have_moved = True

                if tile_have_moved:
                    break

            if not tile_have_moved:
                self.sleep_tile()
        else:
            self.color = self.settle_color

    def wake_up_tile(self):
        self.position_should_be_updated = True

    def sleep_tile(self):
        self.position_should_be_updated = False

    def get_closes_position_that_is_able_to_move(
            self,
            next_positions: List[Tuple[int, int]]
    ) -> Optional[Tuple[int, int]]:
        last_free_position = None
        for position_on_the_way in next_positions:
            if not self.world.is_position_inside_scene(*position_on_the_way):
                break
            tile_in_next_position = self.world.get_tile_at_position(*position_on_the_way)
            if not self.is_denser_than(tile_in_next_position):
                break
            last_free_position = position_on_the_way
        return last_free_position

    def get_indexes_on_the_way_to_next_position(self, direction: Directions) -> List[Tuple[int, int]]:
        return [self.get_next_position(direction, v) for v in range(1, self.velocity)]

    def swap_position(self, position: Tuple[int, int]):
        self.world.swap_tile_at_positions(
            start_position=(self.x, self.y),
            end_position=position
        )

    def move_coordinates_to(self, position: Tuple[int, int]):
        self.x = position[0]
        self.y = position[1]
