import arcade as arc
from arcade.geometry_generic import clamp
from Misc_Functions import tint_image
from math import sin, cos
import Globals
from random import uniform


class FireParticle(arc.FadeParticle):
    def __init__(self, part_dir):
        part_img = tint_image(Globals.PARTICLE_SHAPE, Globals.GRAY)
        texture = arc.Texture(f"fire part", part_img, hit_box_algorithm=None)
        super().__init__(filename_or_texture=texture, change_xy=(part_dir[0], part_dir[1]),
                         lifetime=.5, scale=uniform(.1, .9), start_alpha=200)

    def update(self, delta_time: float = 1 / 60):
        """Advance the Particle's simulation"""
        super().update()
        a = arc.utils.lerp(self.start_alpha,
                           self.end_alpha,
                           self.lifetime_elapsed / self.lifetime_original)
        self.alpha = clamp(a, 0, 255)


class BoostEmitter(arc.Emitter):
    def __init__(self, center_xy, part_dir):
        super().__init__(center_xy=center_xy, emit_controller=arc.EmitBurst(3),
                         particle_factory=lambda emitter: FireParticle(part_dir))


def boost_emit(center_xy, player_angle):
    particle_move_x = sin(player_angle) + uniform(-1, 1)
    particle_move_y = -cos(player_angle) + uniform(-1, 1)
    e = BoostEmitter(center_xy, (particle_move_x, particle_move_y))
    return boost_emit.__doc__, e
