from World import World


class Explosion:

    def __init__(self, center_x: int, center_y: int, radius: int, world: World):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.world = world

    def trigger(self):
        # getting left corner of square, a = 2 * radius
        start_x = self.center_x - self.radius
        start_y = self.center_y - self.radius
        # going for all pixels in that square
        for x in range(start_x, self.center_x + self.radius):
            for y in range(start_y, self.center_y + self.radius):
                if self._is_position_inside_circle(x, y):
                    self.world.remove_tile(x, y)

    def _is_position_inside_circle(self, x: int, y: int):
        # equation of circle: (x - a)^2 + (y - b)^2 = r^2
        return ((x - self.center_x) * (x - self.center_x) + (y - self.center_y) * (
                y - self.center_y)) < self.radius * self.radius
