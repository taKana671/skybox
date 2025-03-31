import sys
from enum import Enum, auto

from direct.actor.Actor import Actor
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletWorld, BulletDebugNode
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import load_prc_file_data
from panda3d.core import NodePath, Point3, Vec3, BitMask32
from panda3d.core import TransformState

# from scene import Scene


load_prc_file_data("", """
    textures-power-2 none
    gl-coordinate-system default
    window-title Panda3D Test Terrain
    filled-wireframe-apply-shader true
    stm-max-views 8
    stm-max-chunk-count 2048""")


class Motions(Enum):

    FORWARD = auto()
    BACKWARD = auto()
    TURN = auto()


class Walker(NodePath):

    RUN = 'run'
    WALK = 'walk'

    def __init__(self):
        h, w = 6, 1.2
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'wolker'))

        self.set_collide_mask(BitMask32.allOn())
        self.set_scale(0.5)
        base.world.attach_character(self.node())

        self.actor = Actor(
            'models/ralph/ralph.egg',
            {self.RUN: 'models/ralph/ralph-run.egg',
             self.WALK: 'models/ralph/ralph-walk.egg'}
        )
        self.actor.set_transform(TransformState.make_pos(Vec3(0, 0, -2.5)))
        self.actor.set_name('ralph')
        self.actor.reparent_to(self)

    def play_anim(self, motion):
        match motion:

            case Motions.FORWARD:
                anim = Walker.RUN

            case Motions.BACKWARD:
                anim = Walker.WALK

            case Motions.TURN:
                anim = Walker.WALK

            case _:
                if self.actor.get_current_anim() is not None:
                    self.actor.stop()
                    self.actor.pose(Walker.WALK, 5)
                return

        if self.actor.get_current_anim() != anim:
            self.actor.loop(anim)


class SkyBoxDemo(ShowBase):

    def __init__(self):
        super().__init__()
        self.disable_mouse()

        self.world = BulletWorld()
        self.world.set_gravity(Vec3(0, 0, -9.81))

        self.debug = self.render.attach_new_node(BulletDebugNode('debug'))
        self.world.set_debug_node(self.debug.node())

        # setup character
        self.walker = Walker()
        self.walker.reparent_to(self.render)
        self.walker.set_pos(Point3(-18.0243, 14.9644, -12.354343))
        self.floater = NodePath('floater')
        self.floater.set_z(3.0)
        self.floater.reparent_to(self.walker)

        # setup camera
        self.camera.reparent_to(self.walker)
        self.camera.set_pos(Vec3(0, 10, 1))
        self.camera.look_at(self.floater)
        self.camLens.set_fov(90)

        self.setup_scene()
        # self.scene = Scene()
        # self.scene.reparent_to(self.render)

        inputState.watch_with_modifiers('forward', 'arrow_up')
        inputState.watch_with_modifiers('backward', 'arrow_down')
        inputState.watch_with_modifiers('left', 'arrow_left')
        inputState.watch_with_modifiers('right', 'arrow_right')

        self.accept('i', self.print_info)
        self.accept('escape', sys.exit)
        self.accept('d', self.toggle_debug)
        self.taskMgr.add(self.update, 'update')

    def print_info(self):
        print(self.walker.get_pos())

    def toggle_debug(self):
        # self.toggle_wireframe()
        if self.debug.is_hidden():
            self.debug.show()
        else:
            self.debug.hide()

    def control_walker(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0
        motion = None

        if inputState.is_set('forward'):
            speed.set_y(-10.0)
            motion = Motions.FORWARD

        if inputState.is_set('backward'):
            speed.set_y(5.0)
            motion = Motions.BACKWARD

        if inputState.is_set('left'):
            omega = 30.0
            motion = Motions.TURN

        if inputState.is_set('right'):
            omega = -30.0
            motion = Motions.TURN

        self.walker.node().set_angular_movement(omega)
        self.walker.node().set_linear_movement(speed, True)
        self.walker.play_anim(motion)

    def update(self, task):
        dt = globalClock.get_dt()
        self.control_walker(dt)
        self.world.do_physics(dt)

        return task.cont