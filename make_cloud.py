import cv2
import numpy as np



def make_cloud(path):
    img = cv2.imread(path)

    size_y, size_x = img.shape[:2]

    for y in range(size_y):
        for x in range(size_x):
            # import pdb; pdb.set_trace()
            if img[y, x, 0] <= 160:
                img[y, x, :] = [250, 206, 135]
                # print(y, x, img[y, x, :])

    cv2.imwrite('cloud.png', img)


def make_cloud_2(path):
    color_img = np.full((256, 256, 3), [250, 206, 135], np.uint8)
    noise = cv2.imread(path)

    mask = noise / 255
    dst = color_img * mask
    cv2.imwrite('cloud.png', dst)


# def make_cloud_3(noise_path):
#     img = cv2.imread(noise_path)
#     minimum = img.min()
#     maximum = img.max()

#     size_y, size_x = img.shape[:2]
#     dst = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

#     for y in range(size_y):
#         for x in range(size_x):
#             v = dst[y, x, 0]
#             dst[y, x, 3] = v
#             dst[y, x, :3] = 255
#             # dst[y, x, 3] = v - minimum
#             # # dst[y, x, 3] = maximum - v

#     diff = maximum - minimum
#     # bg_img = np.full((256, 256, 3), [255, 0, 0], np.uint8)
#     # bg_img = get_gradient_3d(256, 256, (104, 17, 1), (255, 255, 224), (False, False, False))
#     # bg_img = get_gradient_3d(256, 256, (104, 17, 1), (198, 169, 117), (False, False, False))
#     bg_img = get_gradient_3d(256, 256, (240, 176, 0), (255, 236, 183), (False, False, False))

#     for _ in range(2):
#         bg_img = bg_img * (1 - dst[:, :, 3:] / 255) + dst[:, :, :3] * (dst[:, :, 3:] / 255)
#     result = bg_img.astype(np.uint8)

#     # result = bg_img * (1 - dst[:, :, 3:] / 255) + dst[:, :, :3] * (dst[:, :, 3:] / 255)
#     # result = result.astype(np.uint8)

#     cv2.imwrite('result.png', result)

def make_cloud_4(noise_path):
    cloud_img = cv2.imread(noise_path)
    size_y, size_x = cloud_img.shape[:2]
    cloud_img = cv2.cvtColor(cloud_img, cv2.COLOR_BGR2BGRA)
    minimum = cloud_img.min()
    # maximum = img.max()

    # dst = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    for y in range(size_y):
        for x in range(size_x):
            v = cloud_img[y, x, 0]
            cloud_img[y, x, 3] = v - minimum
            # # dst[y, x, 3] = maximum - v

    # mask = cv2.imread('noise_4.png')
    mask = get_gradient_3d(256, 256, (0, 0, 0), (100, 100, 100), (False, False, False))
    mask = mask.astype(np.uint8)
    cv2.imwrite('mask.png', mask)
    # size_y, size_x = mask.shape[:2]
    # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2BGRA)

    # for y in range(size_y):
    #     for x in range(size_x):
    #         v = mask[y, x, 0]
    #         mask[y, x, 3] = v

    cloud_img = mask * (1 - cloud_img[:, :, 3:] / 255) + cloud_img[:, :, :3] * (cloud_img[:, :, 3:] / 255)
    cloud_img = cloud_img.astype(np.uint8)
    # cloud_img = cv2.cvtColor(cloud_img, cv2.COLOR_BGR2BGRA)
    
    cloud_img = cv2.cvtColor(cloud_img, cv2.COLOR_BGR2BGRA)
    minimum = cloud_img.min()
    mx = cloud_img.max()

    for y in range(size_y):
        for x in range(size_x):
            v = cloud_img[y, x, 0]
            cloud_img[y, x, 3] = v - minimum
            # # dst[y, x, 3] = maximum - v


    cv2.imwrite('cloud.png', cloud_img)
    # for y in range(size_y):
    #     for x in range(size_x):
    #         v = cloud_img[y, x, 0]
    #         cloud_img[y, x, 3] = v


    # bg_img = get_gradient_3d(256, 256, (192, 142, 0), (255, 236, 183), (False, False, False))
    bg_img = get_gradient_3d(256, 256, (240, 176, 0), (255, 236, 183), (False, False, False))

    # for _ in range(1):
    #     bg_img = bg_img * (1 - cloud_img[:, :, 3:] / 255) + cloud_img[:, :, :3] * (cloud_img[:, :, 3:] / 255)
    # result = bg_img.astype(np.uint8)
    result = bg_img * (1 - cloud_img[:, :, 3:] / 255) + cloud_img[:, :, :3] * (cloud_img[:, :, 3:] / 255)
    result = result.astype(np.uint8)

    cv2.imwrite('result.png', result)

    # diff = maximum - minimum
    # # bg_img = np.full((256, 256, 3), [255, 0, 0], np.uint8)
    # # bg_img = get_gradient_3d(256, 256, (104, 17, 1), (255, 255, 224), (False, False, False))
    # bg_img = get_gradient_3d(256, 256, (104, 17, 1), (198, 169, 117), (False, False, False))

    # for _ in range(3):
    #     bg_img = bg_img * (1 - dst[:, :, 3:] / 255) + dst[:, :, :3] * (dst[:, :, 3:] / 255)
    # result = bg_img.astype(np.uint8)

    # cv2.imwrite('result.png', result)

def make_cloud_5(noise_path):
    img = cv2.imread(noise_path)
    minimum = img.min()
    maximum = img.max()

    size_y, size_x = img.shape[:2]
    dst = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # dic = {}

    for y in range(size_y):
        for x in range(size_x):
            v = dst[y, x, 0]
          
            # if v > 0:
            #     v = 255 * (v / 255) ** (1.0 / 3)

            dst[y, x, :] = v
            # dst[y, x, :] = 255 * (v / 255) ** (1.0 / 2)
    # import pdb; pdb.set_trace()
            # dst[y, x, 3] = v - minimum
            # # dst[y, x, 3] = maximum - v

    #         if v in dic:
    #             dic[v] = dic[v] + 1
    #         else:
    #             dic[v] = 0

    # print(dic)

    
    cv2.imwrite('dst.png', dst)

    bg_img = np.full((256, 256, 3), [255, 255, 255], np.uint8)
    result = bg_img * (dst[:, :, 3:] / 255) + dst[:, :, :3] * (1 - dst[:, :, 3:] / 255)
    # # result = bg_img * (1 - dst[:, :, 3:] / diff) + dst[:, :, :3] * (dst[:, :, 3:] / diff)
    
    mask = result[:, :, 0]

    # for _ in range(1):
    #     bg_img = bg_img * (1 - cloud_img[:, :, 3:] / 255) + cloud_img[:, :, :3] * (cloud_img[:, :, 3:] / 255)
    # result = bg_img.astype(np.uint8)
    result = bg_img * (1 - mask / 255) + result * (mask / 255)

    result = result.astype(np.uint8)

    cv2.imwrite('result.png', result)


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


# def get_clouds(path):
def get_clouds(img):
    density = 0.5
    sharpness = 0.1

    # img = cv2.imread(path)

    # scale img between 0 and 1
    img = img - img.min()
    img = img / img.max()

    img = 1 - np.e ** (-(img - density) * sharpness)
    img[img < 0] = 0

    # scale between 0 to 255 and quantize
    img = img / img.max()
    # img = img * 255
    img = round_arr(img * 255)

    img = img.astype(np.uint8)
    cv2.imwrite('temp.png', img)

    return img

def pers_clouds(path):
    arr = cv2.imread(path)
    h, w = arr.shape[:2]
    img = get_clouds(arr)
    t = -np.pi / 32

    # p = [
    #     [np.cos(t), np.sin(t), 0.],
    #     [-np.sin(t), np.cos(t), 0.],
    #     [0.001, 0.002, 1.]
    # ]

    # matrix = cv2.getPerspectiveTransform(img, np.array(p))

    # src_pts = np.array([[100, 0], [10, 255], [251, 255], [200, 0]], np.float32)
    src_pts = np.array([[78, 0], [10, 255], [245, 255], [178, 0]], np.float32)
    # src_pts = np.array([[0, 128], [128, 255], [255, 128], [128, 0]], np.float32)


    dst_pts = np.array([[0, 0], [0, 255], [255, 255], [255, 0]], np.float32)
    mat = cv2.getPerspectiveTransform(src_pts, dst_pts)
    pers = cv2.warpPerspective(img/255, mat, (256, 256), flags=cv2.INTER_LINEAR)

    # create and combine background gradient
    ph, pw = pers.shape[:2]
    _, back = np.meshgrid(ph, pw)
    out = pers * 4 * pw + back

    # Fit between 0 and 255 fpr image
    out = out - out.min()
    # out = out / out.max() * 255
    out = round_arr(out / out.max() * 255)
    out = out.astype(np.uint8)

    cv2.imwrite('out.png', out)


def make_cloud_3(noise_path, intensity=1):
    mask = cv2.imread(noise_path)
    height, width = mask.shape[:2]

    wh_img = np.full((height, width, 3), [255, 255, 255], np.uint8)
    bg_img = get_gradient_3d(width, height, (240, 176, 0), (255, 236, 183), (False, False, False))

    for _ in range(intensity):
        bg_img = bg_img * (1 - mask / 255) + wh_img * (mask / 255)

    result = bg_img.astype(np.uint8)
    cv2.imwrite('result.png', result)




if __name__ == '__main__':
    pers_clouds('noise_5.png')
    # get_clouds('out.png')
    make_cloud_3('out.png')
    # arr = get_gradient_3d(256, 256, (104, 17, 1), (198, 169, 117), (False, False, False))
    # cv2.imwrite('bg.png', arr)
    # arr = get_gradient_3d(256, 256, (255, 255, 255), (0, 0, 0), (False, False, False))
    # cv2.imwrite('bg.png', arr)


# >>> maker = fbm(weight=0.5, grid=8)
# >>> arr = maker.noise2()
# >>> create_image_8bit(arr)
