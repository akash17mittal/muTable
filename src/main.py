import multiprocessing
from mock_tap_receiver import MockTapReceiver
from camera import Camera
from calibration import ArucoBasedCalibration


def sender(conn, msgs):
    """
    function to send messages to other end of pipe
    """
    for msg in msgs:
        conn.send(msg)
        print("Sent the message: {}".format(msg))
    conn.close()


def receiver(conn):
    """
    function to print the messages received from other
    end of pipe
    """
    while 1:
        msg = conn.recv()
        if msg == "END":
            break
        print("Received the message: {}".format(msg))


if __name__ == "__main__":

    # creating a tap pipe
    tap_sender_conn, tap_receiver_conn = multiprocessing.Pipe()
    sound_signal_sender, sound_signal_receiver = multiprocessing.Pipe()

    # create camera object
    camera = Camera()

    # Do calibration step
    calibration = ArucoBasedCalibration(camera)
    calibration_matrix = calibration.start_calibrating()

    if calibration_matrix is None:
        print("Couldn't Perform Calibration")
        exit()

    print(calibration_matrix)

    # create tap detector object
    tapDetector = MockTapReceiver(tap_sender_conn)

    tapDetectorProcess = multiprocessing.Process(target=tapDetector.start_receiving, args=())

    # creating new processes
    # p1 = multiprocessing.Process(target=sender, args=(parent_conn, msgs))
    p2 = multiprocessing.Process(target=receiver, args=(tap_receiver_conn,))

    # running processes
    tapDetectorProcess.start()
    p2.start()

    # wait until processes finish
    tapDetectorProcess.join()
    p2.join()