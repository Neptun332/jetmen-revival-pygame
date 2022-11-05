from typing import List, Type

from Directions import Directions
from Tile import Tile
from World import World
from semirandom import randint

TILES: List[Type[Tile]] = []


def add_to_tile_list(tile: Type[Tile]) -> Type[Tile]:
    TILES.append(tile)
    print(f"Added tile {tile.NAME}")
    return tile


@add_to_tile_list
class SandTile(Tile):
    NAME = "Sand"

    POSSIBLE_MOVEMENT = (Directions.DOWN, Directions.DOWN_LEFT, Directions.DOWN_RIGHT)

    def __init__(self, x: int, y: int, world: World):
        super().__init__(
            color=(235 + randint(20), 235 + randint(20), 0 + randint(40)),
            x=x,
            y=y,
            world=world
        )

    def update(self):
        for direction in self.POSSIBLE_MOVEMENT:
            next_position = self.get_next_position(direction)
            # TODO add density for water
            if not self.world.is_position_inside_scene(*next_position):
                continue
            tile_in_next_position = self.world.get_tile_at_position(*next_position)
            if not tile_in_next_position:
                self.move_to_position(next_position)
                break
