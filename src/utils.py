import numpy as np
from cv2 import aruco


def get_aruco_image(width, height):
    image_size = (height, width)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    aruco_image = np.ones(image_size, dtype=np.uint8) * 255

    n = 9
    for i in range(0, n):
        row = i // 3
        col = i % 3
        img = aruco.drawMarker(aruco_dict, i + 1, int(0.3 * width))
        x = int((0.025 * (col + 1) + 0.3 * col) * width)
        y = int((0.025 * (row + 1) + 0.3 * row) * height)
        aruco_image[y:y + img.shape[0], x:x + img.shape[1]] = img

    return aruco_image, aruco_dict