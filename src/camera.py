import pyrealsense2 as rs
import numpy as np


class Camera:

    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        self.pipeline.start(config)

    def get_current_image(self):
        print("Here")
        frames = self.pipeline.wait_for_frames()
        print("There")
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        return color_image
