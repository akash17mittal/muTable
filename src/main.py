import multiprocessing
from multiprocessing.managers import BaseManager
from mock_tap_receiver import start_tap_receiving
from calibration import ArucoBasedCalibration
from depth_calibration import DepthCalibration
from hand_location_detector import start_hand_tracking
from event_manager import start_receving_tap_events_with_location
from instruments.drums.drums import start_playing_drums, Drums
from utils import get_aruco_image
from projection import Projection, start_projecting
from ble_tap_receiver import left_tap_receiver, right_tap_receiver
import cv2

if __name__ == "__main__":

    width = 1920
    height = 1080
    space_for_ui = 0.15
    is_debug_mode = True

    # creating a tap pipe
    tap_sender_conn, tap_receiver_conn = multiprocessing.Pipe()
    sound_signal_sender_conn, sound_signal_receiver_conn = multiprocessing.Pipe()
    tap_location_sender_conn, tap_location_receiver_conn = multiprocessing.Pipe()

    # Do calibration step
    aruco_image, aruco_dict = get_aruco_image(height, height)
    if is_debug_mode:
        cv2.imwrite("markers.jpg", aruco_image)

    drums = Drums(width, height, space_for_ui)
    drum_with_ui_image = drums.get_full_image_with_ui()

    if is_debug_mode:
        cv2.imwrite("./drums.jpg", drum_with_ui_image)

    BaseManager.register('ProjectionData', Projection)
    manager = BaseManager()
    manager.start()
    projectionData = manager.ProjectionData(aruco_image, "L")

    projectionProcess = multiprocessing.Process(target=start_projecting, args=[projectionData])
    projectionProcess.start()

    calibration = ArucoBasedCalibration(aruco_image, aruco_dict)
    calibration_matrix = calibration.start_calibrating()
    calibration.release_resources()

    if calibration_matrix is None:
        print("Couldn't Perform Calibration")
        exit()

    print("Calibration Matrix = ", calibration_matrix)

    projectionData.update_pic(drum_with_ui_image, "RGB")

    depthCalibration = DepthCalibration()
    surface_depth = depthCalibration.start_calibrating()
    depthCalibration.release_resources()

    print("Surface Depth = ", surface_depth)

    # create tap detector object
    # tapDetectorProcess = multiprocessing.Process(target=start_tap_receiving, args=(tap_sender_conn,))
    leftTapDetectorProcess = multiprocessing.Process(target=left_tap_receiver, args=(tap_sender_conn,))
    rightTapDetectorProcess = multiprocessing.Process(target=right_tap_receiver, args=(tap_sender_conn,))

    # create hand location detector
    handLocationDetectionProcess = multiprocessing.Process(target=start_hand_tracking, args=(
        calibration_matrix, surface_depth, tap_receiver_conn, tap_location_sender_conn))

    # start receiving tap events with location
    tapLocationProcess = multiprocessing.Process(target=start_receving_tap_events_with_location, args=(
        width, height, space_for_ui, tap_location_receiver_conn, sound_signal_sender_conn, projectionData))

    # create musical instrument
    instrumentProcess = multiprocessing.Process(target=start_playing_drums,
                                                args=(width, height, sound_signal_receiver_conn))

    # running processes
    leftTapDetectorProcess.start()
    rightTapDetectorProcess.start()
    handLocationDetectionProcess.start()
    tapLocationProcess.start()
    instrumentProcess.start()

    # wait until processes finish
    leftTapDetectorProcess.join()
    rightTapDetectorProcess.join()
    handLocationDetectionProcess.join()
    tapLocationProcess.join()
    instrumentProcess.join()
    projectionProcess.terminate()
