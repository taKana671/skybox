import copy
from datetime import datetime
from enum import Enum

import cv2
import numpy as np

# from NoiseTexture.pynoise.perlin import Perlin
from cynoise.fBm import FractionalBrownianMotion as fbm


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(width, height, starts, stops, is_hors):
    result = np.zeros((height, width, len(starts)), dtype=np.uint8)

    for i, (start, stop, is_horizontal) in enumerate(zip(starts, stops, is_hors)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


def round_arr(x, decimals=0):
    return np.sign(x) * np.floor(np.abs(x) * 10**decimals + 0.5) / 10**decimals


class Sky(Enum):

    SKYBLUE = ([0, 176, 240], [183, 236, 255])
    BLUE = ([1, 17, 104], [117, 169, 198])

    def __init__(self, start_color, end_color):
        self.start = start_color
        self.end = end_color

    def rgb_to_bgr(self):
        idx = [2, 1, 0]
        start_color = [self.start[i] for i in idx]
        end_color = [self.end[i] for i in idx]
        return start_color, end_color


class Cloud:

    def __init__(self, arr):
        self.img = arr

    def output(self, img, output_path):
        img = img.astype(np.uint8)
        cv2.imwrite(output_path, img)

    def generate(self, width=256, height=256, intensity=1, sky_color=Sky.SKYBLUE, bbox=None):
        """Create a cloud image from noise.
            Args:
                width(int): width of the cloud image to be generated.
                height(int): height of the cloud image to be generated.
                intensity(int): white color intensity; minimum = 1
                sky_color(Sky): background gradation
                bbox(list): 4 points of a rectangle in the noise image;
                            must be the format of [[ax, ay], [bx, by], [cx, cy], [dx, dy]].;
                            ax, ay, bx, by, cx, cy, dx, dy: int

                            self.img              transformed in perspective_transform method
                           ________________     a ________________d
                          |     d_____ c   |     |                |
                          |     /    /     |     |                |
                          |    /____/      | --> |                |
                          |   a     b      |     |                |
                          |________________|    b|________________|c
        """
        src_pts = self.get_src_pts(self.img.shape, bbox)
        print(src_pts)
        img = copy.deepcopy(self.img)
        img = self.adjust(img)
        img = self.perspective_transform(img, width, height, src_pts)
        img = self.generate_cloud(img, width, height, intensity, sky_color)
        img = img.astype(np.uint8)

        now = datetime.now()
        file_name = f'cloud_{now.strftime("%Y%m%d%H%M%S")}.png'
        cv2.imwrite(file_name, img)

    def adjust(self, img):
        density = 0.5
        sharpness = 0.1

        img = img - img.min()
        img = img / img.max()
        img = 1 - np.e ** (-(img - density) * sharpness)
        img[img < 0] = 0

        # Scale between 0 to 255 and quantize
        img = img / img.max()
        img = round_arr(img * 255)

        # img = img.astype(np.uint8)
        # cv2.imwrite('temp.png', img)

        return img

    def get_src_pts(self, size, bbox):
        h, w = size[:2]
        w -= 1
        h -= 1

        if bbox is None:
            pt_a = [w * 0.392, 0]
            pt_b = [w * 0.039, h]
            pt_c = [w * 0.96, h]
            pt_d = [w * 0.784, 0]
            return round_arr([pt_a, pt_b, pt_c, pt_d])

        if len(bbox) != 4:
            raise ValueError(f'pts must have 4 elements. got={len(bbox)}.')

        for pt in bbox:
            if len(pt) != 2:
                raise ValueError(f'The length of each element of pts must be 2. got={pt}.')

        return [[min(max(0, pt[0]), w), min(max(0, pt[1]), h)] for pt in bbox]

    def perspective_transform(self, img, width, height, src_pts):
        src_pts = np.array(src_pts, np.float32)
        # src_pts = np.array([[100, 0], [10, 255], [245, 255], [200, 0]], np.float32)

        w, h = width - 1, height - 1
        dst_pts = np.array([[0, 0], [0, h], [w, h], [w, 0]], np.float32)
        mat = cv2.getPerspectiveTransform(src_pts, dst_pts)
        img = cv2.warpPerspective(img, mat, (width, height), flags=cv2.INTER_LINEAR)  # w, h

        img = img - img.min()
        img = round_arr(img / img.max() * 255)

        # img = img.astype(np.uint8)
        # cv2.imwrite('out.png', img)
        return img

    def generate_cloud(self, mask, width, height, intensity, sky_color):
        wh_img = np.full((height, width, 3), [255, 255, 255], np.uint8)
        start_color, end_color = sky_color.rgb_to_bgr()
        bg_img = get_gradient_3d(width, height, start_color, end_color, (False, False, False))

        for _ in range(intensity):
            bg_img = bg_img * (1 - mask / 255) + wh_img * (mask / 255)

        return bg_img

    @classmethod
    def from_file(cls, file_path):
        arr = cv2.imread(file_path)
        return cls(arr)

    @classmethod
    def from_fbm(cls, grid=8, size=256):
        maker = fbm(grid=grid, size=size)
        arr = maker.noise2()
        arr = np.clip(arr * 255, a_min=0, a_max=255).astype(np.uint8)
        arr = np.stack([arr] * 3, axis=2)
        return cls(arr)
