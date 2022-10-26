import numpy as np
import cv2
from cv2 import aruco
import time
from camera import Camera


class ArucoBasedCalibration:

    def __init__(self, aruco_image, aruco_dict):
        # TODO: Camera object should be global
        self.camera = Camera()
        self.aruco_dict = aruco_dict
        self.count_threshold = 6
        self.parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(aruco_image, self.aruco_dict, parameters=self.parameters)
        self.image_plane_coordinates = {}
        for i in range(ids.shape[0]):
            self.image_plane_coordinates[ids[i][0]] = corners[i][0]

        print("Image Plane Coordinates - ", self.image_plane_coordinates)

    def start_calibrating(self, max_tries=3):
        try_count = 0

        while try_count < max_tries:
            curr_image = self.camera.get_current_image()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(curr_image, self.aruco_dict,
                                                                  parameters=self.parameters)
            projected_world_coordinates = np.array((0, 2))
            image_world_coordinates = np.array((0, 2))
            if ids is not None and ids.shape[0] >= self.count_threshold:
                print(ids)
                for i in range(ids.shape[0]):
                    image_world_coordinates = np.vstack([image_world_coordinates, self.image_plane_coordinates[ids[i][0]]])
                    projected_world_coordinates = np.vstack([projected_world_coordinates, corners[i][0]])
                homo_matrix, _ = cv2.findHomography(projected_world_coordinates, image_world_coordinates)
                return homo_matrix
            time.sleep(0.5)
            try_count += 1

        print("Calibration Failed")
        return None

    def release_resources(self):
        self.camera.stop_pipeline()
