import logging
import asyncio
import platform
import ast
import time
from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover
import struct
import numpy as np
import scipy
from numpy import mean
BLE_UUID_TEST_SERVICE     =          "9A48ECBA-2E92-082F-C079-9E75AAE428B1"

BLE_UUID_AMPLITUDE         =         "E3ADBF53-950E-DC1D-9B44-076BE52760D6"

BLE_UUID_FLOAT_VALUE1       =         "C8F88594-2217-0CA6-8F06-A4270B675D69"

BLE_UUID_FLOAT_VALUE2         =       "C8F88594-2217-0CA6-8F06-A4270B675D70"
BLE_UUID_FLOAT_VALUE3     =           "C8F88594-2217-0CA6-8F06-A4270B675D68"

previous_value=0.000000000
current_value=0.0000000000
tol=1e-6
def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    output_numbers = list(data)
    print(output_numbers)

async def run(address):
    previous_value=0.0000000000

    print('ProtoStax Arduino Nano BLE LED Peripheral Central Service')
    print('Looking for Arduino Nano 33 BLE Sense Peripheral Device...')

    found = False

    async with BleakClient(address) as client:
        #await client.is_connected()
        print(f'Connected to {address}')
        found=True


        while True:
            #time.sleep(1)

            #await client.start_notify(BLE_UUID_FLOAT_VALUE, notification_handler)
            #val1 = await client.read_gatt_char(BLE_UUID_FLOAT_VALUE1)
            #val2= await client.read_gatt_char(BLE_UUID_FLOAT_VALUE2)
            val3 = await client.read_gatt_char(BLE_UUID_FLOAT_VALUE3)

            z= struct.unpack('<f', val3)
            current_value=round(z[0],5)

            #print("current value", current_value)
            #print("previous value", previous_value)
            try:

                if(abs(current_value-previous_value)>tol):
                    print("TAP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    previous_value=current_value
            except Exception as e:
                value = str(e).encode()
                print(value)


            print("Z val", z)



    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')





address = "db:eb:8d:2b:72:b9"
loop = asyncio.get_event_loop()


if __name__ == "__main__":
    address = "db:eb:8d:2b:72:b9"
    previous_value = 0.000000000
    print('address:', address)
    loop.run_until_complete(run(address))

