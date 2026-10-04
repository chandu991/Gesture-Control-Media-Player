# media_controller.py

import pyautogui
import time


class MediaController:

    def __init__(self):

        self.last_action_time = 0

        self.action_delay = 0.8

    def can_execute(self):

        current_time = time.time()

        if (
            current_time - self.last_action_time
            >= self.action_delay
        ):

            self.last_action_time = current_time

            return True

        return False

    def play_pause(self):

        if self.can_execute():

            pyautogui.press("playpause")

    def next_track(self):

        if self.can_execute():

            pyautogui.press("nexttrack")

    def previous_track(self):

        if self.can_execute():

            pyautogui.press("prevtrack")

    def volume_up(self):

        if self.can_execute():

            pyautogui.press("volumeup")

    def volume_down(self):

        if self.can_execute():

            pyautogui.press("volumedown")