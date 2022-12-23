from typing import Tuple

from tiles import Tile
from utils.semirandom import randint


# Can be added UnMovingTile parent
class StoneTile(Tile):
    NAME = "Stone"
    DENSITY = 20

    def __init__(self, x: int, y: int, world: 'World', force: Tuple[int, int]):
        super().__init__(
            color=(110 + randint(20), 110 + randint(20), 110 + randint(20)),
            x=x,
            y=y,
            world=world,
            density=self.DENSITY
        )

    def is_movable(self):
        return False
