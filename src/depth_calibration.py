import numpy as np
from camera import Camera


class DepthCalibration:

    def __init__(self):
        # TODO: Camera object should be global
        self.camera = Camera()

    def start_calibrating(self, max_tries=60):
        try_count = 0
        sum_projection_depths = 0.0
        while try_count < max_tries:
            depth_image = self.camera.get_current_depth_image()
            dmap = depth_image.reshape(-1)
            unique, counts = np.unique(dmap[dmap > 1], return_counts=True)
            projection_depth = unique[np.argmax(counts)] * self.camera.depth_scale
            sum_projection_depths += projection_depth
            try_count += 1
        return sum_projection_depths/try_count

    def release_resources(self):
        self.camera.stop_pipeline()
