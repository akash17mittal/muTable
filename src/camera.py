import pyrealsense2 as rs
import numpy as np
import time
import multiprocessing


class Camera:

    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # Start streaming
        profile = self.pipeline.start(config)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale = ", self.depth_scale)

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def get_current_image(self):
        print("Fetch an Image")
        try:
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            return color_image
        except Exception as e:
            raise e

    def get_current_depth_image(self):
        try:
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            return depth_image
        except Exception as e:
            raise e

    def get_color_and_depth_image(self):
        try:
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            depth_frame = aligned_frames.get_depth_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            return color_image, depth_image
        except Exception as e:
            raise e

    def stop_pipeline(self):
        self.pipeline.stop()


def acquire_images():
    camera = Camera()
    while 1:
        img = camera.get_current_image()
        time.sleep(1)


if __name__ == '__main__':
    p = multiprocessing.Process(target=acquire_images, args=())
    p.start()
    while 1:
        time.sleep(1)
