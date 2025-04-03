from skybox_base import SkyBoxDemo
from scene import Scene


class SphereSky(SkyBoxDemo):

    def __init__(self):
        super().__init__()

    def setup_scene(self):
        self.scene = Scene()
        self.scene.reparent_to(self.render)
        self.scene.make_sphere_sky()


if __name__ == '__main__':
    app = SphereSky()
    app.run()