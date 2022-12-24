import math
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
            force: Tuple[int, int]
    ):
        super().__init__(color, x, y, world, density)
        self.settle_color = color
        self.position_should_be_updated = True  # False if tile have neighbours preventing it from moving
        self.tile_have_moved = False
        self.active = True
        self.force = force
        self.update_force(self.force)

    def is_movable(self):
        return True

    def update_position(
            self,
            possible_movement: Tuple[Directions, ...],
            force: Tuple[int, int]
    ):
        if self.position_should_be_updated and self.active:
            self.color = (255, 0, 0)

            self.update_force(force)

            tile_have_moved = self.update_position_according_to_direction(self.force_direction)
            possible_movement = [direction for direction in possible_movement if direction != self.force_direction]
            if not tile_have_moved:
                for direction in possible_movement:
                    tile_have_moved = self.update_position_according_to_direction(direction)

                    if tile_have_moved:
                        break

            if not tile_have_moved:
                self.sleep_tile()
        else:
            self.color = self.settle_color

    def update_force(
            self,
            force: Tuple[int, int]
    ):
        # TODO use numpy to speedup
        self.force = [sum(force_dim) for force_dim in zip(force, self.force)]
        self.force_degrees = self.calculate_vector_degrees(self.force)
        self.force_direction = self.translate_normalized_force_to_direction()
        self.force_magnitude = math.sqrt(sum(f * f for f in self.force))
        self.velocity = int(self.force_magnitude)

    def calculate_vector_degrees(self, vector: Tuple[int, int]):
        # TODO change this to numpy!
        if vector[1] == 0:
            return 1.5 * math.pi
        return math.degrees(math.atan(vector[0] / vector[1]))

    def update_position_according_to_direction(self, direction: Directions) -> bool:
        next_positions = self.get_indexes_on_the_way_to_next_position(direction)
        position_that_is_able_to_move = self.get_closes_position_that_is_able_to_move(next_positions)
        if position_that_is_able_to_move:
            self.swap_position(position_that_is_able_to_move)
            return True
        else:
            self.force = (0, 1)
            self.update_force(self.force)
            return False

    def translate_normalized_force_to_direction(self) -> Directions:
        dirs = [Directions.DOWN, Directions.DOWN_LEFT, Directions.LEFT, Directions.UP_LEFT,
                Directions.UP, Directions.UP_RIGHT, Directions.RIGHT, Directions.DOWN_RIGHT, ]
        ix = round(self.force_degrees / (360. / len(dirs)))
        return dirs[ix % len(dirs)]

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
        return [self.get_next_position(direction, v + 1) for v in range(0, self.velocity)]

    def swap_position(self, position: Tuple[int, int]):
        self.world.swap_tile_at_positions(
            start_position=(self.x, self.y),
            end_position=position
        )

    def move_coordinates_to(self, position: Tuple[int, int]):
        self.x = position[0]
        self.y = position[1]
