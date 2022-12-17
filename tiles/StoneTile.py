from tiles import Tile
from utils.semirandom import randint


class StoneTile(Tile):
    NAME = "Stone"
    DENSITY = 20

    def __init__(self, x: int, y: int, world: 'World', velocity: int):
        super().__init__(
            color=(110 + randint(20), 110 + randint(20), 110 + randint(20)),
            x=x,
            y=y,
            density=self.DENSITY
        )
