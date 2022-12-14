from typing import List, Type

from tiles.MovingTile import Tile
from tiles.SandTile import SandTile
from tiles.StoneTile import StoneTile
from tiles.WaterTile import WaterTile

TILES: List[Type[Tile]] = [SandTile, WaterTile, StoneTile]
