import time

from config import Config
from roboboactions import RoboboActions
from utils import take_screenshot, take_screenshot_sim
from .behaviour import Behaviour
from .sharedclass import SharedClass


class CaptureData(Behaviour):
    """
    A class to capture data from the Robobo robot.

    Attributes:
        roboboactions (RoboboActions): Instance of the RoboboActions class to manage robot actions.
    """

    def __init__(self, robot: RoboboActions, supress_list, params,config):
        """
        Initializes the CaptureData class.

        Args:
            robot (RoboboActions): Instance of the RoboboActions class.
            supress_list (list): List of behaviors to suppress.
            params (dict): Dictionary of parameters.
        """
        super().__init__(robot, supress_list, params)
        self.roboboactions = robot
        self.config = config

    def take_control(self):
        """
        Determines when the behavior should take control.

        Returns:
            bool: Always returns True after a 2-second delay.
        """
        time.sleep(2)
        return True

    def action(self):
        """
        Defines the actions to be taken by the behavior.
        """
        SharedClass.firstscreenshot = True
        print("----> control: ScreenShot")
        sensor_dict = {
            "image_number": SharedClass.img_counter,
            "sensors_data": self.roboboactions.read_sensors()
        }
        SharedClass.sensor_data.append(sensor_dict)

        if self.config.is_simulation():
            take_screenshot_sim()  # for simulation
        else:
            take_screenshot()  # for real
        SharedClass.img_counter += 1
        if SharedClass.img_counter == 10:
            SharedClass.img_counter = 0
            SharedClass.sensor_data.clear()
