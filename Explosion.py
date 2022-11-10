from World import World


class Explosion:

    def __init__(self, center_x: int, center_y: int, radius: int, world: World):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.world = world

    def trigger(self):
        start_x = self.center_x - self.radius
        start_y = self.center_y - self.radius
        for x in range(start_x, self.center_x + self.radius):
            for y in range(start_y, self.center_y + self.radius):
                # equation of circle: (x - a)^2 + (y - b)^2 = r^2
                if ((x - self.center_x) * (x - self.center_x)
                        + (y - self.center_y) * (y - self.center_y)) <= self.radius * self.radius:
                    self.world.remove_tile(x, y)
