import cv2
import numpy as np
from dataclasses import dataclass
from ..circle import Circle


@dataclass
class Piece:
    """Data Class for Sound Event Object"""
    name: str
    shape: Circle
    sound: str


class Drums:

    def __init__(self, width=1080, height=1080):
        self.height = height
        self.width = width
        self.pieces = self.get_drum_pieces(width, height)

    def get_drum_pieces(self, width, height):
        piece_widths = [0.3, 0.23, 0.43]
        angle = np.pi / 6
        piece2_d = 0.03 + piece_widths[1] / 2 + piece_widths[2] / 2
        piece1_x = 0.025 + piece_widths[0] / 2
        piece3_x = 1 - 0.025 - piece_widths[2] / 2
        piece2_x = piece3_x - np.cos(angle) * piece2_d

        piece1_y = 0.45
        piece3_y = 0.45
        piece2_y = piece3_y + np.sin(angle) * piece2_d
        piece_x_coords = np.array([piece1_x, piece2_x, piece3_x]) * width
        piece_y_coords = np.array([piece1_y, piece2_y, piece3_y]) * height
        piece_radius = np.array(piece_widths) * width / 2

        pieces = [Piece(f"Piece{i+1}", Circle((int(piece_x_coords[i]), int(piece_y_coords[i])), int(piece_radius[i])), f"./sound_data/{i + 1}.wav")
                  for i in range(3)]
        return pieces

    def get_image(self):

        image_size = (self.height, self.width, 3)

        yellow_color = (255, 204, 153)
        dark_yellow_color = (255, 153, 51)

        drums = np.zeros(shape=image_size, dtype=np.uint8)
        for piece in self.pieces:
            drums = cv2.circle(drums, piece.shape.center, piece.shape.radius, yellow_color, -1)
            drums = cv2.circle(drums, piece.shape.center, int(piece.shape.radius*2/5), (0, 0, 0), -1)
            drums = cv2.circle(drums, piece.shape.center, piece.shape.radius, dark_yellow_color, int(0.025 * self.width))

        return drums


def start_playing_drums(width, height, sound_signal_receiver_conn):
    drums = Drums(width, height)
    cv2.imwrite("./drums.jpg", drums.get_image())
    while 1:
        sound_event = sound_signal_receiver_conn.recv()
        print("Sound Produced = ", sound_event)