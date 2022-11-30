# https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
import asyncio
from typing import Any
from tap import *
import multiprocessing
from bleak import BleakClient, discover
import struct


class Connection:
    client: BleakClient = None

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            read_characteristic: str,
            tap_sender_conn,
            arduino_mac: str,
            hand
    ):
        self.loop = loop
        self.read_characteristic = read_characteristic
        self.connected = False
        self.connected_device = None
        self.tap_sender_conn = tap_sender_conn
        self.arduino_mac = arduino_mac
        self.hand = hand

    def on_disconnect(self, client: BleakClient, future: asyncio.Future):
        self.connected = False
        # Put code here to handle what happens on disconnet.
        print(f"Disconnected from {self.connected_device}!")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(self.read_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(15.0, loop=self.loop)

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, self.notification_handler,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(3.0, loop=self.loop)
            else:
                print(f"Failed to connect to {self.connected_device}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        await asyncio.sleep(2.0, loop=self.loop)  # Wait for BLE to initialize.
        devices = await discover()
        discovered_devices_macs = []

        for i, device in enumerate(devices):
            discovered_devices_macs.append(device.address)
            print(f"{i}: {device.address}")

        if str.upper(self.arduino_mac) not in discovered_devices_macs:
            print("Device Not Found")
            return

        print(f"Connecting to {self.arduino_mac}")
        self.connected_device = self.arduino_mac
        self.client = BleakClient(self.arduino_mac, loop=self.loop)

    def notification_handler(self, sender: str, data: Any):
        tap_detected = struct.unpack('<f', data)
        print("Data from - ", sender, " is = ", tap_detected)
        print(tap_detected)
        self.tap_sender_conn.send(Tap(self.hand, tap_detected))


def left_tap_receiver(tap_sender_conn):
    read_characteristic = "C8F88594-2217-0CA6-8F06-A4270B675D68"
    left_arduino_mac = "5d:c8:38:fd:3c:2f"
    # Create the event loop.
    loop = asyncio.get_event_loop()

    connection = Connection(
        loop, read_characteristic, tap_sender_conn, left_arduino_mac, Hand.LEFT
    )
    try:
        asyncio.ensure_future(connection.manager())
        loop.run_forever()
    except KeyboardInterrupt:
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())


def right_tap_receiver(tap_sender_conn):
    read_characteristic = "C8F88594-2217-0CA6-8F06-A4270B675D68"
    right_arduino_mac = "24:55:06:86:c2:a3"
    # Create the event loop.
    loop = asyncio.get_event_loop()

    connection = Connection(
        loop, read_characteristic, tap_sender_conn, right_arduino_mac, Hand.RIGHT
    )
    try:
        asyncio.ensure_future(connection.manager())
        loop.run_forever()
    except KeyboardInterrupt:
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(connection.cleanup())


if __name__ == '__main__':
    tap_sender_conn, tap_receiver_conn = multiprocessing.Pipe()
    leftTapDetectorProcess = multiprocessing.Process(target=left_tap_receiver, args=(tap_sender_conn,))
    leftTapDetectorProcess.start()
    leftTapDetectorProcess.join()
