import arcade as arc
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
import Globals
from Player import BasicPlayer


def new_area(game):
    area_pymunk(game)


def area_one(game):
    game.scene = arc.Scene()
    game.scene.add_sprite_list("player")

    game.player = BasicPlayer()
    game.scene.add_sprite("player", game.player)

    game.camera = arc.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
    game.gui_camera = arc.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
    game.physics_engine = arc.PhysicsEngineSimple(game.player, [])


def area_pymunk(game):
    game.camera = arc.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
    game.gui_camera = arc.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
    game.physics_engine = arc.PymunkPhysicsEngine(damping=Globals.DAMPING, gravity=Globals.GRAVITY)

    game.scene = arc.Scene()
    game.scene.add_sprite_list("player")
    game.scene.add_sprite_list_after("tests", "player")

    game.player = BasicPlayer()
    game.scene.add_sprite("player", game.player)
    game.physics_engine.add_sprite(game.player, friction=Globals.P_FRICTION,
                                   moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                   damping=0.01, collision_type="player", max_velocity=400)
    game.player.pymunk_phys = game.physics_engine.get_physics_object(game.player)



