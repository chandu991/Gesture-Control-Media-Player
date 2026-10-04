# gesture_detector.py

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from config import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE
)


class GestureDetector:

    def __init__(self):

        # Path to the MediaPipe hand model
        model_path = "models/hand_landmarker.task"

        # Create MediaPipe base options
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        # Configure Hand Landmarker
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=MAX_HANDS,
            min_hand_detection_confidence=DETECTION_CONFIDENCE,
            min_hand_presence_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )

        # Create hand landmarker
        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

    def detect_hand(self, frame):

        # OpenCV uses BGR
        # MediaPipe expects RGB

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert NumPy/OpenCV image to MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        results = self.detector.detect(mp_image)

        return results

    def draw_landmarks(self, frame, results):

        if results.hand_landmarks:

            for hand_landmarks in results.hand_landmarks:

                # Convert normalized coordinates
                # into actual image coordinates

                height, width, _ = frame.shape

                points = []

                for landmark in hand_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    points.append((x, y))

                    # Draw landmark
                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Hand connections
                connections = [
                    (0, 1),
                    (1, 2),
                    (2, 3),
                    (3, 4),

                    (0, 5),
                    (5, 6),
                    (6, 7),
                    (7, 8),

                    (5, 9),
                    (9, 10),
                    (10, 11),
                    (11, 12),

                    (9, 13),
                    (13, 14),
                    (14, 15),
                    (15, 16),

                    (13, 17),
                    (17, 18),
                    (18, 19),
                    (19, 20),

                    (0, 17)
                ]

                for start, end in connections:

                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 0, 0),
                        2
                    )

        return frame

    def count_fingers(self, hand_landmarks):

        fingers = []

        # --------------------------------
        # INDEX FINGER
        # --------------------------------

        if hand_landmarks[8].y < hand_landmarks[6].y:

            fingers.append(1)

        else:

            fingers.append(0)

        # --------------------------------
        # MIDDLE FINGER
        # --------------------------------

        if hand_landmarks[12].y < hand_landmarks[10].y:

            fingers.append(1)

        else:

            fingers.append(0)

        # --------------------------------
        # RING FINGER
        # --------------------------------

        if hand_landmarks[16].y < hand_landmarks[14].y:

            fingers.append(1)

        else:

            fingers.append(0)

        # --------------------------------
        # LITTLE FINGER
        # --------------------------------

        if hand_landmarks[20].y < hand_landmarks[18].y:

            fingers.append(1)

        else:

            fingers.append(0)

        return fingers

    def recognize_gesture(self, hand_landmarks):

        fingers = self.count_fingers(
            hand_landmarks
        )

        total_fingers = sum(fingers)

        # Fist
        if total_fingers == 0:

            return "FIST"

        # One finger
        elif total_fingers == 1:

            return "PLAY_PAUSE"

        # Two fingers
        elif total_fingers == 2:

            return "NEXT"

        # Three fingers
        elif total_fingers == 3:

            return "PREVIOUS"

        # Four fingers
        elif total_fingers == 4:

            return "VOLUME_UP"

        # Five fingers
        elif total_fingers == 5:

            return "VOLUME_UP"

        else:

            return "UNKNOWN"

    def close(self):

        self.detector.close()