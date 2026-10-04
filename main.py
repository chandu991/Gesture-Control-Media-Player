# main.py

import cv2

from gesture_detector import GestureDetector
from media_controller import MediaController

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    WINDOW_NAME,
    GESTURE_STABLE_FRAMES
)


def main():

    # -----------------------------------------
    # 1. OPEN WEBCAM
    # -----------------------------------------

    camera = cv2.VideoCapture(CAMERA_INDEX)

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )


    # -----------------------------------------
    # 2. CHECK CAMERA
    # -----------------------------------------

    if not camera.isOpened():

        print("ERROR: Could not open webcam.")

        return


    # -----------------------------------------
    # 3. CREATE GESTURE DETECTOR
    # -----------------------------------------

    detector = GestureDetector()


    # -----------------------------------------
    # 4. CREATE MEDIA CONTROLLER
    # -----------------------------------------

    media_controller = MediaController()


    # -----------------------------------------
    # 5. GESTURE VARIABLES
    # -----------------------------------------

    previous_gesture = None

    stable_count = 0

    current_gesture = "NONE"


    # -----------------------------------------
    # 6. START MESSAGE
    # -----------------------------------------

    print("----------------------------------------")
    print("Gesture Controlled Media Player")
    print("----------------------------------------")
    print("Starting camera...")
    print()

    print("Gestures:")
    print("1 Finger  -> Play/Pause")
    print("2 Fingers -> Next Track")
    print("3 Fingers -> Previous Track")
    print("5 Fingers -> Volume Up")
    print("Fist      -> Volume Down")
    print()

    print("Press Q to exit.")
    print("----------------------------------------")


    # -----------------------------------------
    # 7. MAIN LOOP
    # -----------------------------------------

    while True:


        # -------------------------------------
        # CAPTURE CAMERA FRAME
        # -------------------------------------

        success, frame = camera.read()


        if not success:

            print(
                "ERROR: Could not read webcam frame."
            )

            break


        # -------------------------------------
        # MIRROR CAMERA
        # -------------------------------------

        frame = cv2.flip(
            frame,
            1
        )


        # -------------------------------------
        # DETECT HAND
        # -------------------------------------

        results = detector.detect_hand(
            frame
        )


        # -------------------------------------
        # DRAW LANDMARKS
        # -------------------------------------

        frame = detector.draw_landmarks(
            frame,
            results
        )


        # -------------------------------------
        # DEFAULT GESTURE
        # -------------------------------------

        detected_gesture = "NONE"


        # -------------------------------------
        # CHECK HAND
        # -------------------------------------

        if results.hand_landmarks:


            # Get first detected hand

            hand_landmarks = (
                results.hand_landmarks[0]
            )


            # ---------------------------------
            # RECOGNIZE GESTURE
            # ---------------------------------

            detected_gesture = (
                detector.recognize_gesture(
                    hand_landmarks
                )
            )


        # -------------------------------------
        # GESTURE STABILITY
        # -------------------------------------

        if (
            detected_gesture
            == previous_gesture
        ):

            stable_count += 1


        else:

            previous_gesture = (
                detected_gesture
            )

            stable_count = 0


        # -------------------------------------
        # EXECUTE GESTURE
        # -------------------------------------

        if (
            stable_count
            == GESTURE_STABLE_FRAMES
        ):


            current_gesture = (
                detected_gesture
            )


            # ---------------------------------
            # PLAY / PAUSE
            # ---------------------------------

            if detected_gesture == "PLAY_PAUSE":

                media_controller.play_pause()


            # ---------------------------------
            # NEXT TRACK
            # ---------------------------------

            elif detected_gesture == "NEXT":

                media_controller.next_track()


            # ---------------------------------
            # PREVIOUS TRACK
            # ---------------------------------

            elif detected_gesture == "PREVIOUS":

                media_controller.previous_track()


            # ---------------------------------
            # VOLUME UP
            # ---------------------------------

            elif detected_gesture == "VOLUME_UP":

                media_controller.volume_up()


            # ---------------------------------
            # VOLUME DOWN
            # ---------------------------------

            elif detected_gesture == "FIST":

                media_controller.volume_down()


        # -------------------------------------
        # DISPLAY CURRENT GESTURE
        # -------------------------------------

        cv2.putText(

            frame,

            f"Gesture: {current_gesture}",

            (30, 50),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0, 255, 0),

            2

        )


        # -------------------------------------
        # DISPLAY INSTRUCTIONS
        # -------------------------------------

        cv2.putText(

            frame,

            "Q = Quit",

            (30, 90),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )


        # -------------------------------------
        # DISPLAY CAMERA
        # -------------------------------------

        cv2.imshow(

            WINDOW_NAME,

            frame

        )


        # -------------------------------------
        # KEYBOARD INPUT
        # -------------------------------------

        key = cv2.waitKey(1) & 0xFF


        # -------------------------------------
        # EXIT
        # -------------------------------------

        if key == ord("q"):

            break


    # -----------------------------------------
    # 8. RELEASE CAMERA
    # -----------------------------------------

    camera.release()


    # -----------------------------------------
    # 9. CLOSE WINDOWS
    # -----------------------------------------

    cv2.destroyAllWindows()


    # -----------------------------------------
    # 10. CLOSE MEDIAPIPE
    # -----------------------------------------

    detector.close()


    print("Program stopped.")


# ---------------------------------------------
# START PROGRAM
# ---------------------------------------------

if __name__ == "__main__":

    main()