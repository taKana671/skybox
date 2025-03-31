from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletHeightfieldShape, ZUp
from panda3d.core import NodePath, BitMask32, Point3, PandaNode
from panda3d.core import Filename, PNMImage
from panda3d.core import Shader, TextureStage, TexGenAttrib
from panda3d.core import GeoMipTerrain
from panda3d.core import Camera

from shapes.src import Sphere, Box


class Terrain(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('terrain'))
        self.heightmap = 'terrains/heightmap.png'
        self.height = 20
        self.node().set_mass(0)
        self.set_collide_mask(BitMask32.bit(1))
        shape = BulletHeightfieldShape(base.loader.load_texture(self.heightmap), self.height, ZUp)
        shape.set_use_diamond_subdivision(True)
        self.node().add_shape(shape)
        self.generate_terrain()

    def generate_terrain(self):
        img = PNMImage(Filename(self.heightmap))
        self.terrain = GeoMipTerrain('geomip_terrain')
        self.terrain.set_heightfield(self.heightmap)
        self.terrain.set_border_stitching(True)
        self.terrain.set_block_size(8)
        self.terrain.set_min_level(2)
        self.terrain.set_focal_point(base.camera)
        self.terrain.setBruteforce("True")

        size_x, size_y = img.get_size()
        x = (size_x - 1) / 2
        y = (size_y - 1) / 2
        # x = size_x / 2 - 0.5
        # y = size_y / 2 - 0.5

        pos = Point3(-x, -y, -(self.height / 2))
        self.root = self.terrain.get_root()
        self.root.set_sz(self.height)
        self.root.set_pos(pos)
        self.terrain.generate()
        self.root.reparent_to(self)

        shader = Shader.load(Shader.SL_GLSL, 'shaders/terrain_v.glsl', 'shaders/terrain_f.glsl')
        self.root.set_shader(shader)

        for i, file_name in enumerate(['grass_02.png', 'grass_01.jpg']):
            ts = TextureStage(f'ts{i}')
            ts.set_sort(i)
            self.root.set_shader_input(f'tex_ScaleFactor{i}', 20)
            tex = base.loader.load_texture(f'textures/{file_name}')
            self.root.set_texture(ts, tex)


class Building(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('building'))
        box = Box(20, 20, 20).create()
        box.reparent_to(self)

        end, tip = box.get_tight_bounds()
        size = tip - end
        shape = BulletBoxShape(size / 2)
        self.node().add_shape(shape)
        self.set_collide_mask(BitMask32.bit(1))

        tex = base.loader.load_texture('textures/tile_01.jpg')
        self.set_texture(tex)


class CubeMapSkyBox(NodePath):

    def __init__(self):
        super().__init__(PandaNode('skybox_root'))
        self.make_skybox()

    def make_skybox(self):
        self.sphere = Sphere(radius=500).create()
        self.sphere.set_pos(0, 0, 0)
        self.sphere.reparent_to(self)

        ts = TextureStage.get_default()
        self.sphere.set_tex_gen(ts, TexGenAttrib.M_world_cube_map)
        self.sphere.set_tex_hpr(ts, (0, 180, 0))
        self.sphere.set_tex_scale(ts, (1, -1))

        self.sphere.set_light_off()
        self.sphere.set_material_off()
        imgs = base.loader.load_cube_map('textures/skybox/img_#.png')
        self.sphere.set_texture(imgs)


class DisplayRegionSkyBox(NodePath):

    def __init__(self):
        super().__init__(PandaNode('skybox_root'))
        self.make_skybox()

    def make_skybox(self):
        self.skybox_region = base.win.make_display_region(0, 1, 0, 1)
        # cam = base.makeCamera(base.win)
        cam = Camera('skybox_cam')
        self.skybox_cam = NodePath(cam)
        # if set custom lens, sky follows character.
        self.skybox_cam.node().set_lens(base.camLens)
        self.skybox_cam.reparent_to(self)
        self.skybox_region.set_camera(self.skybox_cam)

        self.skybox_region.setSort(-1000)
        # self.skybox_region.setSort(5)
        # base.win.get_display_region(1).setSort(10)
        # base.win.get_display_region(2).setSort(25)

        self.box = Box(1000, 1000, 1000).create()
        self.box.set_pos(0, 0, 0)
        # self.box.set_light_off()
        # self.box.set_material_off()
        self.box.reparent_to(self)

        tex = base.loader.load_texture('textures/cloud.png')
        self.box.set_texture(tex)


class Scene(NodePath):

    def __init__(self):
        super().__init__(PandaNode('scene'))
        self.ground = Terrain()
        self.ground.reparent_to(self)
        base.world.attach(self.ground.node())
        self.ground.set_z(-12)

        self.building = Building()
        self.building.reparent_to(self)
        base.world.attach(self.building.node())
        self.building.set_pos(Point3(-18.0243, -52.54451, -12.036247))

        # print(base.win.getActiveDisplayRegions())
        # (DisplayRegion(0 1 0 1)=pixels(0 800 0 600), DisplayRegion(0 1 0 1)=pixels(0 800 0 600), DisplayRegion(0 1 0 1)=pixels(0 800 0 600))

    def make_cubemap_skybox(self):
        self.skybox = CubeMapSkyBox()
        self.skybox.reparent_to(self)
        self.skybox.set_pos(0, 0, 150)

    def make_display_region_skybox(self):
        # Do not parent to base.render
        self.skybox = DisplayRegionSkyBox()
        self.skybox.set_pos(0, 0, 150)
