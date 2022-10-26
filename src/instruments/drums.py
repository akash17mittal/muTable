import cv2
import numpy as np


class Drums:

    def __init__(self, width=1080, height=1080):
        self.height = height
        self.width = width

    def get_image(self):
        width = self.width
        height = self.height

        image_size = (height, width, 3)

        piece_widths = [0.3, 0.23, 0.43]
        angle = np.pi / 6
        piece2_d = 0.03 + piece_widths[1] / 2 + piece_widths[2] / 2
        piece1_x = 0.025 + piece_widths[0] / 2
        piece3_x = 1 - 0.025 - piece_widths[2] / 2
        piece2_x = piece3_x - np.cos(angle) * piece2_d

        piece1_y = 0.45
        piece3_y = 0.45
        piece2_y = piece3_y + np.sin(angle) * piece2_d
        piece_x_coords = [piece1_x, piece2_x, piece3_x]
        piece_y_coords = [piece1_y, piece2_y, piece3_y]

        yellow_color = (255, 204, 153)
        dark_yellow_color = (255, 153, 51)

        drums = np.zeros(shape=image_size, dtype=np.uint8)
        for i in [0, 1, 2]:
            drums = cv2.circle(drums, (int(piece_x_coords[i] * width), int(piece_y_coords[i] * height)),
                               int(width * piece_widths[i] / 2), yellow_color, -1)
            drums = cv2.circle(drums, (int(piece_x_coords[i] * width), int(piece_y_coords[i] * height)),
                               int(width * piece_widths[i] / 5), (0, 0, 0), -1)
            drums = cv2.circle(drums, (int(piece_x_coords[i] * width), int(piece_y_coords[i] * height)),
                               int(width * piece_widths[i] / 2), dark_yellow_color, int(0.025 * width))