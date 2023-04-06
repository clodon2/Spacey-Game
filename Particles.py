import arcade as arc
from math import sin, cos
import Globals
from random import uniform, choice


RED_PART_TEXTURE = arc.Texture(f"red part01", Globals.red_part, hit_box_algorithm=None)
ORANGE_PART_TEXTURE = arc.Texture(f"orange part02", Globals.orange_part, hit_box_algorithm=None)
YELLOW_PART_TEXTURE = arc.Texture(f"yellow part03", Globals.yellow_part, hit_box_algorithm=None)
GRAY_PART_TEXTURE = arc.Texture(f"gray part04", Globals.gray_part, hit_box_algorithm=None)


class BoostParticle(arc.FadeParticle):
    def __init__(self, part_dir):
        part_img = choice([RED_PART_TEXTURE, ORANGE_PART_TEXTURE, YELLOW_PART_TEXTURE, GRAY_PART_TEXTURE])
        texture = part_img
        super().__init__(filename_or_texture=texture, change_xy=(part_dir[0], part_dir[1]),
                         lifetime=.5, scale=uniform(.1, .9), start_alpha=200)


class BoostEmitter(arc.Emitter):
    def __init__(self, center_xy, part_dir):
        super().__init__(center_xy=center_xy, emit_controller=arc.EmitBurst(3),
                         particle_factory=lambda emitter: BoostParticle(part_dir))


def boost_emit(center_xy, player_angle):
    particle_move_x = sin(player_angle) + uniform(-1, 1)
    particle_move_y = -cos(player_angle) + uniform(-1, 1)
    e = BoostEmitter(center_xy, (particle_move_x, particle_move_y))
    return boost_emit.__doc__, e
