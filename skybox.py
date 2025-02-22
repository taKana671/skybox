import sys

from direct.showbase.ShowBase import ShowBase
from shapes.src import Box, Sphere
from panda3d.core import PerspectiveLens, Camera
from panda3d.core import Texture, TextureStage, TexGenAttrib
from panda3d.core import TexturePool



class MySkyBox(ShowBase):

    def __init__(self):
        super().__init__()
        self.disable_mouse()
        # self.camera.set_pos(0, -10, 0)
        self.camera.set_pos(0, 0, -10)
        self.camera.look_at(0, 0, 0)

        box = Box(0.5, 0.5, 0.5).create()
        box.set_pos_hpr((0, 0, 0), (45, 30, 0))
        box.set_color(1, 0, 0, 1)
        box.reparent_to(self.render)

        # self.create_skybox()
        # self.create_skybox_by_displayregion()
        # self.create_skybox_by_cubemap()
        self.create_skybox_by_cubemap()
        self.accept('escape', sys.exit)

    def create_skybox(self):
        self.skybox = Box().create()
        self.skybox.set_pos(0, 0, 0)
        self.skybox.set_scale(2000)
        self.skybox.set_texture(self.loader.load_texture('sky-material-24-cl.png'))
        self.skybox.reparent_to(self.render)
        self.skybox.set_shader_off()
        self.skybox.set_bin('background', 0)
        self.skybox.set_depth_write(0)
        self.skybox.set_light_off()

    def create_skybox_by_displayregion(self):
        self.skybox = Box().create()
        self.skybox.set_pos(0, 0, 0)
        self.skybox.set_scale(2000)

        self.camNode.get_display_region(0).set_sort(1)
        view = self.win.make_display_region(0, 1, 0, 1)
        view.set_sort(0)

        lens = PerspectiveLens()
        new_cam = Camera('skybox_camera', lens)
        sky_cam = self.skybox.attach_new_node(new_cam)
        del new_cam
        del lens

        view.set_camera(sky_cam)
        # self.camNode.set_active(False)

    def create_skybox_by_cubemap(self):
        tex = Texture('world_cube_map')
        tex.setup_cube_map()
        tex.read(fullpath='sky/img_0.png', z=0, n=0, read_pages=False, read_mipmaps=False)
        tex.read(fullpath='sky/img_1.png', z=1, n=0, read_pages=False, read_mipmaps=False)
        tex.read(fullpath='sky/img_5.png', z=2, n=0, read_pages=False, read_mipmaps=False)
        tex.read(fullpath='sky/img_4.png', z=3, n=0, read_pages=False, read_mipmaps=False)
        tex.read(fullpath='sky/img_2.png', z=4, n=0, read_pages=False, read_mipmaps=False)
        tex.read(fullpath='sky/img_3.png', z=5, n=0, read_pages=False, read_mipmaps=False)
        TexturePool.add_texture(tex)

        ts = TextureStage.get_default()
        self.skybox = Sphere().create()
        self.skybox.set_scale(2)
        self.skybox.reparent_to(self.render)
        self.skybox.set_texture(tex)

        self.skybox.set_tex_gen(ts, TexGenAttrib.M_world_cube_map)
        # self.skybox.set_tex_hpr(ts, (0, 0, 0))
        # self.skybox.set_tex_hpr(ts, (0, 90, 180))
        self.skybox.set_tex_scale(ts, (1, -1))
        self.skybox.set_light_off()
        self.skybox.set_material_off()


        # ###################################################
        # self.sphere = Box().create()
        # self.sphere.set_pos_hpr((0, 0, 0), (45, 30, 0))
        # self.sphere = Sphere().create()
        # self.sphere.set_pos(0, 0, 0)
        # self.sphere.set_scale(5)
        # cubemap = self.loader.load_cube_map('sky/img_#.png')
        # self.sphere.set_texture(cubemap)
        # self.sphere.reparent_to(self.render)






if __name__ == '__main__':
    skybox = MySkyBox()
    skybox.run()