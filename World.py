from typing import List, Tuple

from Tile import Tile


class World:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles: List[Tile] = []
        self.moving_tiles: List[Tile] = []
        init_matrix: List[List[Tile or None]] = []
        for _ in range(height):
            init_matrix.append([None for _ in range(width)])
        self.spatial_matrix: Tuple[List[Tile], ...] = tuple(init_matrix)

    def add_tile(self, tile_type: type, x: int, y: int) -> Tile:
        """ adds a tile at the given position and returns it """
        new_tile: Tile = tile_type(x, y, self)
        if not self.spatial_matrix[y][x]:
            self.tiles.append(new_tile)
            self.moving_tiles.append(new_tile)
            self.spatial_matrix[y][x] = new_tile
        return new_tile

    def update(self):
        for tile in self.moving_tiles:
            tile.update()

    def get_tile_at_position(self, x: int, y: int):
        return self.spatial_matrix[y][x]

    def move_tile_from_one_position_to_other(self, start_position: Tuple[int, int], end_position: Tuple[int, int]):
        tile = self.spatial_matrix[start_position[1]][start_position[0]]
        self.spatial_matrix[start_position[1]][start_position[0]] = None
        self.spatial_matrix[end_position[1]][end_position[0]] = tile

    def is_position_inside_scene(self, x: int, y: int) -> bool:
        if not 0 <= x < self.width:
            return False
        if not 0 <= y < self.height:
            return False
        return True
