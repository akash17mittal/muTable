import multiprocessing
from mock_tap_receiver import MockTapReceiver
from camera import Camera
from calibration import ArucoBasedCalibration
from hand_location_detector import HandLocationDetector
from instruments.drums import Drums

if __name__ == "__main__":
    # multiprocessing.set_start_method('forkserver')

    # creating a tap pipe
    tap_sender_conn, tap_receiver_conn = multiprocessing.Pipe()
    sound_signal_sender_conn, sound_signal_receiver_conn = multiprocessing.Pipe()

    # create camera object
    camera = Camera()

    # Do calibration step
    calibration = ArucoBasedCalibration(camera)
    calibration_matrix = calibration.start_calibrating()

    # if calibration_matrix is None:
    #     print("Couldn't Perform Calibration")
    #     exit()

    print(calibration_matrix)

    # create tap detector object
    tapDetector = MockTapReceiver(tap_sender_conn)
    tapDetectorProcess = multiprocessing.Process(target=tapDetector.start_receiving, args=())

    # create hand location detector
    handLocationDetector = HandLocationDetector(camera, calibration_matrix, tap_receiver_conn, sound_signal_sender_conn)
    handLocationDetectionProcess = multiprocessing.Process(target=handLocationDetector.start_hand_tracking, args=())

    # create musical instrument
    instrument = Drums(1080, 1080, sound_signal_receiver_conn)
    instrumentProcess = multiprocessing.Process(target=instrument.start_producing_sound, args=())

    # running processes
    tapDetectorProcess.start()
    handLocationDetectionProcess.start()
    instrumentProcess.start()

    # wait until processes finish
    tapDetectorProcess.join()
    handLocationDetectionProcess.join()
    instrumentProcess.start()
