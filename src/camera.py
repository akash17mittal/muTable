import pyrealsense2 as rs
import numpy as np
import time
import multiprocessing


class Camera:

    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        self.pipeline.start(config)

    def get_current_image(self):
        print("Fetch an Image")
        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            print("Color Image Retrieved Successfully")
            return color_image
        except Exception as e:
            raise e

    def stop_pipeline(self):
        self.pipeline.stop()


def acquire_images(arr):
    print(arr)
    camera = Camera()
    while 1:
        img = camera.get_current_image()
        time.sleep(1)


if __name__ == '__main__':
    a = np.zeros(10)
    p = multiprocessing.Process(target=acquire_images, args=(a,))
    p.start()
    while 1:
        time.sleep(1)
