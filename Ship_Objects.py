import arcade as arc
from math import sin, cos, degrees


class BasicPart(arc.SpriteSolidColor):
    def __init__(self):
        super().__init__(25, 25, arc.color.RED)
        self.parent = None
        self.pymunk_phys = None

    def move_with_parent(self):
        if self.parent:
            x = self.parent.center_x + (-sin(self.parent.pymunk_phys.body.angle) * self.width/2)
            y = self.parent.center_y + (cos(self.parent.pymunk_phys.body.angle) * self.height/2)
            self.center_x = x
            self.center_y = y

            self.angle = self.parent.angle

    def on_update(self, delta_time: float = 1 / 60):
        # update pymunk physics and usual variables with pymunk ones
        if self.pymunk_phys:
            self.angle += degrees(self.change_angle)
            self.pymunk_phys.body.angle += self.change_angle
            print(self.angle, self.pymunk_phys.body.angle)

            # prevent player from going outside area
            self.pymunk_phys.body._set_position((self.center_x, self.center_y))
