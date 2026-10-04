# Gesture Control Media player

A Python-based computer vision project that allows users to control media playback using hand gestures.

## Features

- Play/Pause media
- Next track
- Previous track
- Volume up
- Volume down
- Real-time hand detection
- Real-time gesture recognition

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## Project Structure

Gesture Control Media Player/

├── main.py
├── gesture_detector.py
├── media_controller.py
├── config.py
├── requirements.txt
└── README.md

## Installation

Install Python.

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Run

python main.py

## Controls

1 Finger  -> Play/Pause

2 Fingers -> Next Track

3 Fingers -> Previous Track

5 Fingers -> Volume Up

Fist      -> Volume Down

Press Q to exit.

## How It Works

Webcam
↓
OpenCV
↓
MediaPipe
↓
Hand Landmark Detection
↓
Finger Detection
↓
Gesture Recognition
↓
Media Command
↓
Media Player

## Author

Chandra Sekhar