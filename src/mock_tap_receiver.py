import time
from tap import *


class MockTapReceiver:

    def __init__(self, tap_sender_pipe_connection):
        print("Initialize Bluetooth and all")
        self.tap_sender_pipe_connection = tap_sender_pipe_connection

    def start_receiving(self):
        print("Start Receiving Tap Events")
        while 1:
            print("Sending Tap Event")
            self.tap_sender_pipe_connection.send(Tap(Hand.LEFT, 0.1))
            time.sleep(1)


def start_tap_receiving(tap_sender_conn):
    tapDetector = MockTapReceiver(tap_sender_conn)
    tapDetector.start_receiving()
