from enum import Enum, auto

from direct.actor.Actor import Actor
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import NodePath, TransformState
from panda3d.core import Vec2, Vec3, BitMask32

from panda3d.bullet import BulletCharacterControllerNode


class Motions(Enum):

    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    TURN = auto()


class Walker(NodePath):

    RUN = 'run'
    WALK = 'walk'

    def __init__(self):
        # super().__init__(BulletRigidBodyNode('wolker'))
        h, w = 6, 1.2
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'wolker'))
        
        # self.node().add_shape(shape)
        # self.node().set_kinematic(True)
        # self.node().set_ccd_motion_threshold(1e-7)
        # self.node().set_ccd_swept_sphere_radius(0.5)
        # self.set_collide_mask(BitMask32.bit(1))
        self.set_collide_mask(BitMask32.allOn())
        self.set_scale(0.5)
        # base.world.attach(self.node())
        base.world.attach_character(self.node())

        self.actor = Actor(
            'models/ralph/ralph.egg',
            {self.RUN: 'models/ralph/ralph-run.egg',
             self.WALK: 'models/ralph/ralph-walk.egg'}
        )
        self.actor.set_transform(TransformState.make_pos(Vec3(0, 0, -2.5)))
        self.actor.set_name('ralph')
        self.actor.reparent_to(self)

    def check_downward(self, from_pos, distance=-10):
        to_pos = from_pos + Vec3(0, 0, distance)

        if (hit := base.world.ray_test_closest(
                from_pos, to_pos, BitMask32.bit(1))).has_hit():
            return hit

        return None

    def update(self, dt, key_inputs):
        direction = Vec2()
        motion = None

        if Motions.LEFT in key_inputs:
            direction.x += 1
            motion = Motions.TURN

        if Motions.RIGHT in key_inputs:
            direction.x -= 1
            motion = Motions.TURN

        if Motions.FORWARD in key_inputs:
            direction.y += -1
            motion = Motions.FORWARD

        if Motions.BACKWARD in key_inputs:
            direction.y += 1
            motion = Motions.BACKWARD

        self.turn(direction, dt)
        self.move(direction, dt)
        self.play_anim(motion)

    def turn(self, direction, dt):
        if direction.x:
            angle = 100 * direction.x * dt
            self.set_h(self.get_h() + angle)

    def move(self, direction, dt):
        if not direction.y:
            return

        current_pos = self.get_pos()
        speed = 10 if direction.y < 0 else 5
        orientation = self.get_quat(base.render).get_forward()
        next_pos = current_pos + orientation * direction.y * speed * dt

        if not (downward_hit := self.check_downward(next_pos)):
            return

        hit_z = downward_hit.get_hit_pos().z
        next_pos.z = hit_z + 1.2
        self.set_pos(next_pos)

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