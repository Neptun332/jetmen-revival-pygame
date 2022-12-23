from typing import Tuple

from Directions import Directions
from tiles.MovingTile import MovingTile
from utils.semirandom import randint


class WaterTile(MovingTile):
    NAME = "Water"
    DENSITY = 5
    POSSIBLE_MOVEMENT = (
        Directions.DOWN, Directions.DOWN_LEFT, Directions.DOWN_RIGHT, Directions.LEFT, Directions.RIGHT)

    def __init__(self, x: int, y: int, world: 'World', force: Tuple[int, int]):
        super().__init__(
            color=(0 + randint(20), 40 + randint(20), 235 + randint(20)),
            x=x,
            y=y,
            world=world,
            density=self.DENSITY,
            force=force
        )

    def update(self, force: Tuple[int, int]):
        self.update_position(self.POSSIBLE_MOVEMENT, force)
