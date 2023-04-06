import arcade as arc
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
import Globals
from math import degrees


class BasicPlayer(arc.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png")
        self.children = []
        self.scale = .3 * Globals.SCREEN_PERCENT
        self.angle = -90
        self.speed = 0
        self.power_up = None
        self.pymunk_phys = None

    def on_update(self, delta_time: float = 1 / 60):
        # Keep player in bounds
        if self.center_x < 0:
            self.center_x = 0
        if self.center_y < 0:
            self.center_y = 0

        if self.center_x > Globals.AREA_WIDTH:
            self.center_x = Globals.AREA_WIDTH
        if self.center_y > Globals.AREA_HEIGHT:
            self.center_y = Globals.AREA_HEIGHT

        if self.center_x < 0:
            self.center_x = 0
        if self.center_y < 0:
            self.center_y = 0

        # update pymunk physics and usual variables with pymunk ones
        if self.pymunk_phys:
            self.angle += degrees(self.change_angle)
            self.pymunk_phys.body.angle += self.change_angle
            print(self.angle, self.pymunk_phys.body.angle)

            # prevent player from going outside area
            self.pymunk_phys.body._set_position((self.center_x, self.center_y))

        # update children parts to player
        for child in self.children:
            try:
                child.move_with_parent()
            except:
                pass
