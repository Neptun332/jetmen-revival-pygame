from typing import List, Tuple, Optional

from tiles.MovingTile import Tile, MovingTile


class World:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles: List[Tile] = []
        self.moving_tiles: List[MovingTile] = []

        self.tiles_to_add: List[Tile] = []
        self.moving_tiles_to_add: List[Tile] = []

        self.tiles_to_remove: List[Tile] = []
        self.moving_tiles_to_remove: List[Tile] = []

        init_matrix: List[List[Tile or None]] = []
        for _ in range(height):
            init_matrix.append([None for _ in range(width)])
        self.spatial_matrix: Tuple[List[Tile], ...] = tuple(init_matrix)

        self.gravity = 5
        self.gravity_force = (0, 1)

    def add_tile(self, tile_type: type, x: int, y: int):
        if self.is_position_inside_scene(x=x, y=y) and not self.spatial_matrix[y][x]:
            new_tile: Tile = tile_type(x, y, self, self.gravity_force)
            self.tiles_to_add.append(new_tile)
            if issubclass(new_tile.__class__, MovingTile):
                self.moving_tiles_to_add.append(new_tile)
            self.spatial_matrix[y][x] = new_tile

    def remove_tile(self, x: int, y: int):
        if self.is_position_inside_scene(x=x, y=y) and self.spatial_matrix[y][x]:
            tile_to_remove = self.spatial_matrix[y][x]
            tile_to_remove.deactivate()
            self.tiles_to_remove.append(tile_to_remove)
            self.moving_tiles_to_remove.append(tile_to_remove)
            self.spatial_matrix[y][x] = None

    def update(self):
        self.tiles += self.tiles_to_add
        self.tiles_to_add.clear()
        self.moving_tiles += self.moving_tiles_to_add
        self.moving_tiles_to_add.clear()

        self.tiles = [tile for tile in self.tiles if tile not in self.tiles_to_remove]
        self.tiles_to_remove.clear()
        self.moving_tiles = [tile for tile in self.moving_tiles if tile not in self.moving_tiles_to_remove]
        self.moving_tiles_to_remove.clear()

    def update_moving(self):
        for tile in self.moving_tiles:
            tile.update(self.gravity_force)

    def get_tile_at_position(self, x: int, y: int) -> Optional[Tile]:
        return self.spatial_matrix[y][x]

    def move_tile_from_one_position_to_other(self, start_position: Tuple[int, int], end_position: Tuple[int, int]):
        tile = self.spatial_matrix[start_position[1]][start_position[0]]
        self.spatial_matrix[start_position[1]][start_position[0]] = None
        self.spatial_matrix[end_position[1]][end_position[0]] = tile

    def swap_tile_at_positions(self, start_position: Tuple[int, int], end_position: Tuple[int, int]):
        tile = self.spatial_matrix[start_position[1]][start_position[0]]
        end_position_tile = self.spatial_matrix[end_position[1]][end_position[0]]

        if tile:
            tile.wake_up_neighbours()
            tile.move_coordinates_to(end_position)

        if end_position_tile:
            end_position_tile.wake_up_tile()
            end_position_tile.wake_up_neighbours()
            end_position_tile.move_coordinates_to(start_position)

        self.spatial_matrix[start_position[1]][start_position[0]] = end_position_tile
        self.spatial_matrix[end_position[1]][end_position[0]] = tile

    def is_position_inside_scene(self, x: int, y: int) -> bool:
        if not 0 <= x < self.width:
            return False
        if not 0 <= y < self.height:
            return False
        return True
