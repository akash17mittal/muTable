import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
from sound_event import SoundEvent
from camera import Camera


class HandLocationDetector:

    def __init__(self, calibratrion_matrix, tap_receiver_conn, sound_event_sender_conn):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.tap_receiver_conn = tap_receiver_conn
        self.sound_event_sender_conn = sound_event_sender_conn
        self.calibration_matrix = calibratrion_matrix
        # TODO : Camera object should be shared as it is used by multiple modules
        self.camera = Camera()

    def start_hand_tracking(self):
        while 1:
            detected_tap = self.tap_receiver_conn.recv()
            print("Received the message: {}".format(detected_tap))
            curr_image = self.camera.get_current_image()
            curr_image.flags.writeable = False
            curr_image = cv2.cvtColor(curr_image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(curr_image)
            curr_image.flags.writeable = True
            if results.multi_handedness:
                handedness = [handedness.classification[0].label for handedness in results.multi_handedness]
                print(handedness)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hand_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * 640)
                    hand_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * 480)
                    hand_coordinates = np.dot(self.calibration_matrix, np.array([hand_x, hand_y, 1]))
                    hand_coordinates = hand_coordinates / hand_coordinates[2]
                    self.sound_event_sender_conn.send(
                        SoundEvent(detected_tap.intensity, hand_coordinates[0], hand_coordinates[1]))


def start_hand_tracking(calibration_matrix, tap_receiver_conn, sound_signal_sender_conn):
    handLocationDetector = HandLocationDetector(calibration_matrix, tap_receiver_conn, sound_signal_sender_conn)
    handLocationDetector.start_hand_tracking()
