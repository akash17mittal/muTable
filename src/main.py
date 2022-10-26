import multiprocessing
from mock_tap_receiver import start_tap_receiving
from calibration import ArucoBasedCalibration
from hand_location_detector import start_hand_tracking
from instruments.drums.drums import start_playing_drums

if __name__ == "__main__":

    width = 1080
    height = 1080

    # creating a tap pipe
    tap_sender_conn, tap_receiver_conn = multiprocessing.Pipe()
    sound_signal_sender_conn, sound_signal_receiver_conn = multiprocessing.Pipe()

    # Do calibration step
    calibration = ArucoBasedCalibration(width, height)
    calibration_matrix = calibration.start_calibrating()
    calibration.release_resources()

    # if calibration_matrix is None:
    #     print("Couldn't Perform Calibration")
    #     exit()

    print(calibration_matrix)

    # create tap detector object
    tapDetectorProcess = multiprocessing.Process(target=start_tap_receiving, args=(tap_sender_conn,))

    # create hand location detector
    handLocationDetectionProcess = multiprocessing.Process(target=start_hand_tracking, args=(calibration_matrix, tap_receiver_conn, sound_signal_sender_conn))

    # create musical instrument
    instrumentProcess = multiprocessing.Process(target=start_playing_drums, args=(width, height, sound_signal_receiver_conn))

    # running processes
    tapDetectorProcess.start()
    handLocationDetectionProcess.start()
    instrumentProcess.start()

    # wait until processes finish
    tapDetectorProcess.join()
    handLocationDetectionProcess.join()
    instrumentProcess.start()
