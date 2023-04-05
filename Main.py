import arcade as arc
import Globals
import Levels as lvl
from Misc_Functions import get_turn_multiplier
from Particles import boost_emit


class GameView(arc.View):
    def __init__(self):
        super().__init__()
        self.width = Globals.SCREEN_WIDTH
        self.height = Globals.SCREEN_HEIGHT

        self.scene = None

        self.camera = None
        self.gui_camera = None
        self.view_left = 0
        self.view_bottom = 0
        self.map_width = Globals.AREA_WIDTH
        self.map_height = Globals.AREA_HEIGHT

        self.player = None

        # input stuff
        self.controller = None

        self.right_trigger_pressed = False
        self.left_trigger_pressed = False

        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.thumbstick_rotation = 0

        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        self.powerup_pressed = False

        # game stuff
        self.game_timer = 0
        self.emitters = []
        self.physics_engine = None

        # resources
        self.background = arc.load_texture(":resources:images/backgrounds/stars.png")

    def process_keychange(self):
        # print(self.controller.x)

        if self.player is None:
            return

        if self.controller:
            self.thumbstick_rotation = self.controller.x
        else:
            self.thumbstick_rotation = 0

        # Process left/right
        if self.w_pressed or self.up_pressed or self.right_trigger_pressed:
            self.move_up = True
        else:
            self.move_up = False

        if self.s_pressed or self.down_pressed or self.left_trigger_pressed:
            self.move_down = True
        else:
            self.move_down = False

        if self.a_pressed or self.left_pressed or self.thumbstick_rotation < -Globals.DEADZONE:
            self.move_left = True
        else:
            self.move_left = False

        if self.d_pressed or self.right_pressed or self.thumbstick_rotation > Globals.DEADZONE:
            self.move_right = True
        else:
            self.move_right = False

        if self.move_up and not self.move_down:
            force = (0, Globals.P_MOVE_FORCE)
            self.physics_engine.apply_force(self.player, force)
            emit_label, emit_emit = boost_emit((self.player.center_x, self.player.center_y),
                                               self.player.pymunk_phys.body.angle)
            self.emitters.append(emit_emit)
        elif self.move_down and not self.move_up:
            force = (0, -Globals.P_MOVE_FORCE)
            self.physics_engine.apply_force(self.player, force)

        controller_rotation_mult = 1

        if self.thumbstick_rotation != 0:
            controller_rotation_mult = abs(self.thumbstick_rotation)

        if self.move_right and not self.move_left:
            self.player.change_angle = -Globals.PLAYER_ROTATION_SPEED
        elif self.move_left and not self.move_right:
            self.player.change_angle = Globals.PLAYER_ROTATION_SPEED
        elif not self.move_left and not self.move_right:
            self.player.change_angle = 0

        if self.powerup_pressed:
            self.powerup_pressed = False

    def on_key_press(self, key, modifiers):
        if key == arc.key.W:
            self.w_pressed = True
        if key == arc.key.S:
            self.s_pressed = True
        if key == arc.key.A:
            self.a_pressed = True
        if key == arc.key.D:
            self.d_pressed = True

        if key == arc.key.UP:
            self.up_pressed = True
        if key == arc.key.DOWN:
            self.down_pressed = True
        if key == arc.key.LEFT:
            self.left_pressed = True
        if key == arc.key.RIGHT:
            self.right_pressed = True

        if key == arc.key.ESCAPE:
            arc.exit()

        if key == arc.key.SPACE:
            self.powerup_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arc.key.W:
            self.w_pressed = False
        if key == arc.key.S:
            self.s_pressed = False
        if key == arc.key.A:
            self.a_pressed = False
        if key == arc.key.D:
            self.d_pressed = False

        if key == arc.key.UP:
            self.up_pressed = False
        if key == arc.key.DOWN:
            self.down_pressed = False
        if key == arc.key.LEFT:
            self.left_pressed = False
        if key == arc.key.RIGHT:
            self.right_pressed = False

        if key == arc.key.SPACE:
            self.powerup_pressed = False

        self.process_keychange()

    # noinspection PyMethodMayBeStatic
    def on_joybutton_press(self, joystick, button):

        if button == 7:  # Right Trigger
            self.right_trigger_pressed = True
        elif button == 6:  # Left Trigger
            self.left_trigger_pressed = True
        elif button == 3:  # "X" Button
            self.powerup_pressed = True

    # noinspection PyMethodMayBeStatic
    def on_joybutton_release(self, joystick, button):

        if button == 7:  # Right Trigger
            self.right_trigger_pressed = False
        elif button == 6:  # Left Trigger
            self.left_trigger_pressed = False
        elif button == 3:  # "X" Button
            self.powerup_pressed = False

    def on_show_view(self):
        arc.set_viewport(0, self.window.width, 0, self.window.height)

        controllers = arc.get_game_controllers()

        if controllers:
            self.controller = controllers[0]
            self.controller.open()
            self.controller.push_handlers(self)

        self.load_level()

    def load_level(self):
        lvl.new_area(self)

    def on_resize(self, width: int, height: int):
        Globals.resize_screen(width, height)
        self.__init__()
        self.on_show_view()

    def on_draw(self):
        self.clear()
        if self.camera is None:
            return

        self.camera.use()

        arc.draw_lrwh_rectangle_textured(0, 0, Globals.AREA_WIDTH, Globals.AREA_HEIGHT, self.background)
        for e in self.emitters:
            e.draw()
        self.scene.draw()

        # gui cam stuff
        self.gui_camera.use()

    def center_camera_to_player(self):
        # Scroll left
        left_boundary = self.view_left + Globals.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left

        # Scroll right
        right_boundary = self.view_left + self.width - Globals.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - Globals.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + Globals.BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

        # keeps camera in left bound of map
        if self.view_left < 0:
            self.view_left = 0

        # keeps camera in right bound of map
        if (self.view_left + self.width) > self.map_width:
            self.view_left = self.map_width - self.width

        # keeps camera in bottom bound of map
        if self.view_bottom < 0:
            self.view_bottom = 0

        # keeps camera in top bound of map
        if self.view_bottom + self.height > self.map_height:
            self.view_bottom = self.map_height - self.height

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera.move_to(position, Globals.CAMERA_SPEED)

        # OLD
        '''''
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )

        self.camera.move_to((screen_center_x, screen_center_y))
        '''''

    def on_update(self, delta_time: float):
        self.game_timer += delta_time

        self.process_keychange()
        self.scene.on_update()
        self.physics_engine.step()
        for emitter in self.emitters:
            emitter.update()

        self.center_camera_to_player()


def main():
    """Main function"""
    window = arc.Window(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.SCREEN_TITLE,
                        fullscreen=False, resizable=True, vsync=False)
    start_view = GameView()
    window.show_view(start_view)
    arc.run()


if __name__ == "__main__":
    main()
