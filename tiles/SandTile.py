from Directions import Directions
from tiles.MovingTile import MovingTile
from utils.semirandom import randint


class SandTile(MovingTile):
    NAME = "Sand"
    DENSITY = 10
    POSSIBLE_MOVEMENT = (Directions.DOWN, Directions.DOWN_LEFT, Directions.DOWN_RIGHT)

    def __init__(self, x: int, y: int, world: 'World', velocity):
        super().__init__(
            color=(235 + randint(20), 235 + randint(20), 0 + randint(40)),
            x=x,
            y=y,
            world=world,
            velocity=velocity,
            density=self.DENSITY
        )

    def update(self):
        self.update_position(self.POSSIBLE_MOVEMENT)
