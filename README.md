# MuTable: Musical Table
Turn any surface into a musical instrument.

# Hardware
- Projector
- Depth Camera (Intel RealSense)
- 2 Arduino Nano 33 BLE

# Instructions

## Hardware Setup
- Connect Projector and Camera to the laptop/desktop and keep it fixed for the session.

<img src="./assets/setup2.jpg" alt="Mount for Projector and Camera" width="300"/>


## Installation Instructions
- Replace the mac addresses of the motion sensing bands with your own bands [Right Band](https://github.com/akash17mittal/muTable/blob/main/src/ble_tap_receiver.py#L113) and [Left Band](https://github.com/akash17mittal/muTable/blob/main/src/ble_tap_receiver.py#L94) here. 
- `pip3 install -r requirements.txt`
- Program the arduino/motion sensing bands using `tapDetection/BLEArduino/BLEArduino.ino`
- Run `python3 src/main.py`
- Wait for about 30 seconds for the system to auto-calibrate and motion sensing bands to get connected to the system.

[![ArUco marker based camera calibration](https://img.youtube.com/vi/orv01SSwh58/0.jpg)](https://youtu.be/orv01SSwh58)

## Code Overview
- Instrument specific code is here: `src/instruments`
- Sound bank is stored here: `src/instruments/drums/sound_data`
- Camera specific configuration is here: `src/camera.py` Current configuration is based on Intel Realsense camera.

# System Overview and Demo
[![Mutable System Overview and Demo](https://img.youtube.com/vi/Gw5PWL1ZBjk/0.jpg)](https://www.youtube.com/watch?v=Gw5PWL1ZBjk&list=PLX5OEonfMsZr1u8KjgrY1cMp8poRRv-LF&index=8)

# User Studies

### User Study 1
[![User Study 1](https://img.youtube.com/vi/jDGnFMR6C9o/0.jpg)](https://youtu.be/jDGnFMR6C9o)

### User Study 2
[![User Study 2](https://img.youtube.com/vi/N4G_yXEIZEw/0.jpg)](https://youtu.be/N4G_yXEIZEw)

### User Study 3
[![User Study 3](https://img.youtube.com/vi/jGTT_nC8-Ss/0.jpg)](https://youtu.be/jGTT_nC8-Ss)
 