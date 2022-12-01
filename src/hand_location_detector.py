import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
from sound_event import TapLocationEvent
from camera import Camera
from tap import *


class HandLocationDetector:

    def __init__(self, calibratrion_matrix, surface_depth, tap_receiver_conn, tap_location_sender_conn):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.tap_receiver_conn = tap_receiver_conn
        self.tap_location_sender_conn = tap_location_sender_conn
        self.calibration_matrix = calibratrion_matrix
        self.surface_depth = surface_depth
        # TODO : Camera object should be shared as it is used by multiple modules
        self.camera = Camera()

    def start_hand_tracking(self):
        while 1:
            detected_tap = self.tap_receiver_conn.recv()
            print("Received the message: {}".format(detected_tap))
            curr_image, curr_depth_image = self.camera.get_color_and_depth_image()
            curr_image.flags.writeable = False
            curr_image = cv2.cvtColor(curr_image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(curr_image)
            curr_image.flags.writeable = True
            if results.multi_handedness:
                handedness = [handedness.classification[0].label for handedness in results.multi_handedness]
                print(handedness)
            index_found = -1
            if detected_tap.hand == Hand.LEFT and "Right" in handedness:
                index_found = handedness.index("Right")
            elif detected_tap.hand == Hand.RIGHT and "Left" in handedness:
                index_found = handedness.index("Left")
            if results.multi_hand_landmarks and index_found != -1:
                # for hand_landmarks in results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[index_found]
                hand_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * 640)
                hand_y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * 480)
                hand_coordinates = np.dot(self.calibration_matrix, np.array([hand_x, hand_y, 1]))
                hand_coordinates = hand_coordinates / hand_coordinates[2]

                print("Hand Coordinates - ", hand_coordinates)

                min_hand_x = 640
                max_hand_x = 0
                min_hand_y = 480
                max_hand_y = 0
                sum_depth_of_landmarks = 0
                count_landmarks = 0
                depth_hand = 0.0
                for landmark in hand_landmarks.landmark:
                    x = min(int(landmark.x * 640), 639)
                    y = min(int(landmark.y * 480), 479)
                    min_hand_x = min(x, min_hand_x)
                    max_hand_x = max(x, max_hand_x)
                    min_hand_y = min(y, min_hand_y)
                    max_hand_y = max(y, max_hand_y)
                    if curr_depth_image[y, x] > 0:
                        sum_depth_of_landmarks += curr_depth_image[y, x]
                        count_landmarks += 1
                if count_landmarks > 0:
                    depth_hand = sum_depth_of_landmarks * self.camera.depth_scale / count_landmarks
                    print("Depth of Hand - ", depth_hand)
                if abs(depth_hand - self.surface_depth) < 0.1:
                    self.tap_location_sender_conn.send(TapLocationEvent(detected_tap.intensity, hand_coordinates[0], hand_coordinates[1]))


def start_hand_tracking(calibration_matrix, surface_depth, tap_receiver_conn, tap_location_sender_conn):
    handLocationDetector = HandLocationDetector(calibration_matrix, surface_depth, tap_receiver_conn, tap_location_sender_conn)
    handLocationDetector.start_hand_tracking()
