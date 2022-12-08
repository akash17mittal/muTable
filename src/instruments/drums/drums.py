import cv2
import numpy as np
from dataclasses import dataclass
from ..circle import Circle
from sound_event import SoundEvent
import soundfile as sf
from .ui import UI
import pathlib
import time
from _thread import *


def update_pair_pics(projectorData, firstPic, secondPic):
    projectorData.update_pic(firstPic, "RGB")
    time.sleep(0.5)
    projectorData.update_pic(secondPic, "RGB")


@dataclass
class Piece:
    """Data Class for Sound Event Object"""
    name: str
    shape: Circle
    sound: tuple


class Drums:

    def __init__(self, width=1920, height=1080, space_for_ui=0.15):
        self.height = height
        self.width = width
        self.space_for_ui = space_for_ui
        self.pieces = self.get_drum_pieces(width, height, space_for_ui)
        ui = UI(width, height, space_for_ui)
        self.ui_image = ui.get_ui_image()
        self.highlighted_images_with_ui = self.get_highlighted_images()
        self.full_image_with_ui = self.get_full_image_with_ui()

    def get_drum_pieces(self, width, height, space_for_ui):
        piece_widths = np.array([0.3, 0.23, 0.43]) * (1 - space_for_ui)
        angle = np.pi * 0.25
        piece2_d = 0.03 + piece_widths[2] / 2 + piece_widths[2] / 2
        piece1_x = 0.025 + piece_widths[0] / 2
        piece3_x = 1 - space_for_ui - 0.025 - piece_widths[2] / 2
        piece2_x = piece3_x - np.cos(angle) * piece2_d

        piece1_y = 0.45
        piece3_y = 0.45
        piece2_y = piece3_y + np.sin(angle) * piece2_d
        piece_x_coords = np.array([piece1_x, piece2_x, piece3_x]) * width
        piece_y_coords = np.array([piece1_y, piece2_y, piece3_y]) * height
        piece_radius = np.array(piece_widths) * width / 2
        sound_path = f"{pathlib.Path(__file__).parent.resolve()}/sound_data"
        print(sound_path)
        pieces = [Piece(f"Piece{i + 1}",
                        Circle((int(piece_x_coords[i]), int(piece_y_coords[i])), int(piece_radius[i])),
                        sf.read(f"{sound_path}/{i + 1}.wav", dtype='float32'))
                  for i in range(3)]
        return pieces

    def get_image(self):

        image_size = (self.height, self.width, 3)

        yellow_color = (255, 204, 153)
        dark_yellow_color = (255, 153, 51)

        drums = np.zeros(shape=image_size, dtype=np.uint8)
        for piece in self.pieces:
            drums = cv2.circle(drums, piece.shape.center, piece.shape.radius, yellow_color, -1)
            drums = cv2.circle(drums, piece.shape.center, int(piece.shape.radius * 2 / 5), (0, 0, 0), -1)
            drums = cv2.circle(drums, piece.shape.center, piece.shape.radius, dark_yellow_color,
                               int(0.025 * self.width))

        return drums

    def get_full_image_with_ui(self):
        return self.ui_image + self.get_image()

    def get_highlighted_images(self, ui_image=None):
        base_drum_image = self.get_image()
        image_size = (self.height, self.width, 3)
        highlighted_images = {}
        for piece in self.pieces:
            drums_highlighted = np.zeros(shape=image_size, dtype=np.uint8)
            drums_highlighted = cv2.circle(drums_highlighted, piece.shape.center, piece.shape.radius, (255, 255, 255), -1)
            highlighted_piece = cv2.addWeighted(base_drum_image, 0.5, drums_highlighted, 0.5, 1.0)
            highlighted_images[piece.name] = highlighted_piece
            if ui_image is not None:
                highlighted_images[piece.name] += ui_image
        return highlighted_images

    def play_sound_from_point(self, sound_event, projectionData=None):
        import sounddevice as sd
        for piece in self.pieces:
            if piece.shape.is_point_inside((sound_event.locationX, sound_event.locationY)):
                amplifier = 1.0
                if abs(sound_event.intensity) < 1.2:
                    amplifier = amplifier/2
                # play_till = {"Piece1": 40000, "Piece2": 8000, "Piece3": 40000}
                # sd.play(piece.sound[0][:play_till[piece.name]], piece.sound[1])
                sd.play(piece.sound[0]*amplifier, piece.sound[1])
                if projectionData is not None:
                    update_pair_pics(projectionData, self.highlighted_images_with_ui[piece.name], self.full_image_with_ui)


def start_playing_drums(width, height, sound_signal_receiver_conn, projectionData):
    drums = Drums(width, height)
    while 1:
        print("Playing drums")
        sound_event = sound_signal_receiver_conn.recv()
        print("Produce Sound = ", sound_event)
        drums.play_sound_from_point(sound_event, projectionData)


def start_playing_dummy_drums(width, height, sound_signal_receiver_conn):
    drums = Drums(width, height)
    pieces = drums.pieces
    while 1:
        for i in range(2):
            drums.play_sound_from_point(SoundEvent(0.1, pieces[2].shape.center[0], pieces[2].shape.center[1]))
            time.sleep(0.3)
            drums.play_sound_from_point(SoundEvent(0.1, pieces[0].shape.center[0], pieces[0].shape.center[1]))
            time.sleep(0.3)
        for i in range(2):
            drums.play_sound_from_point(SoundEvent(0.1, pieces[1].shape.center[0], pieces[1].shape.center[1]))
            time.sleep(0.3)
            drums.play_sound_from_point(SoundEvent(0.1, pieces[0].shape.center[0], pieces[0].shape.center[1]))
            time.sleep(0.3)
