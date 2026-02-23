import time
from threading import Thread

from robobopy.Robobo import Robobo


class Behaviour(Thread):
    """
    A class that inherits from Thread and manages the behavior threads,
    ensuring the architecture functions correctly.

    Attributes:
        robot (Robobo): Instance of the Robobo class.
        supress_list (list): List of behaviors to suppress.
        params (dict): Dictionary of parameters.
    """

    def __init__(self, robot, supress_list, params, **kwargs):
        """
        Initializes the Behaviour class.

        Args:
            robot (Robobo): Instance of the Robobo class.
            supress_list (list): List of behaviors to suppress.
            params (dict): Dictionary of parameters.
            **kwargs: Additional keyword arguments for the Thread class.
        """
        super().__init__(**kwargs)
        self.robot: Robobo = robot
        self.__supress = False
        self.supress_list = supress_list
        self.params = params

    def take_control(self):
        """
        Determines when the behavior should take control.
        """
        pass

    def action(self):
        """
        Defines the actions to be taken by the behavior.
        """
        pass

    def run(self):
        """
        Runs the behavior thread, checking if the behavior should take control
        and executing the action if it does.
        """
        while not self.params["stop"]:
            while not self.take_control() and not self.params["stop"]:
                time.sleep(0.01)
            if not self.params["stop"]:
                self.action()

    @property
    def supress(self):
        """
        bool: Gets or sets the suppression state of the behavior.
        """
        return self.__supress

    @supress.setter
    def supress(self, state):
        self.__supress = state

    def set_stop(self):
        """
        Sets the stop parameter to True, terminating the mission.
        """
        self.params["stop"] = True

    def stopped(self):
        """
        Checks if the stop parameter is set to True.

        Returns:
            bool: True if the stop parameter is set to True, False otherwise.
        """
        return self.params["stop"]