import cv2
import numpy as np
from instruments.rectangle import Rectangle


class UI:

    def __init__(self, width=1920, height=1080, space_for_ui=0.15):
        self.height = height
        self.width = width
        self.space_for_ui = space_for_ui
        self.pieces = self.get_ui_pieces(width, height, space_for_ui)

    def get_ui_pieces(self, width, height, space_for_ui):
        learnTopLeft = (int(0.86 * width), int(0.3 * height))
        learnBottomRight = (int((1 - 0.025) * width), int(0.42 * height))
        textCoordinates = (int(0.868 * width), int(0.38 * height))
        return [("LEARN", Rectangle(learnTopLeft, learnBottomRight), textCoordinates)]

    def get_ui_image(self):
        image_size = (self.height, self.width, 3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        color = (1, 1, 1)
        thickness = 5
        yellow_color = (255, 204, 153)

        ui = np.zeros(shape=image_size, dtype=np.uint8)
        for piece in self.pieces:
            ui = cv2.rectangle(ui, piece[1].topLeft, piece[1].bottomRight, yellow_color, -1)
            ui = cv2.putText(ui, piece[0], piece[2], font, fontScale, color, thickness, cv2.LINE_AA)
            ui[piece[1].topLeft[1]:piece[1].bottomRight[1], piece[1].topLeft[0]:piece[1].bottomRight[0], :] = cv2.rotate(ui[piece[1].topLeft[1]:piece[1].bottomRight[1], piece[1].topLeft[0]:piece[1].bottomRight[0], :], cv2.ROTATE_180)
        return ui
