import time

from api_openai import generate_response
from behaviour_mod.behaviour import Behaviour
from behaviour_mod.sharedclass import SharedClass
from roboboactions import RoboboActions
from template import rules, phases, question, general_description, robot_information
from utils import load_image


class Feedback(Behaviour):
    """
    A class to handle feedback behavior for the Robobo robot.

    Attributes:
        roboboactions (RoboboActions): Instance of the RoboboActions class to manage robot actions.
    """

    def __init__(self, robot: RoboboActions, supress_list, params):
        """
        Initializes the Feedback class.

        Args:
            robot (RoboboActions): Instance of the RoboboActions class.
            supress_list (list): List of behaviors to suppress.
            params (dict): Dictionary of parameters.
        """
        super().__init__(robot, supress_list, params)
        self.roboboactions = robot

    def take_control(self):
        """
        Determines when the behavior should take control.

        Returns:
            bool: True if the first screenshot has been taken and the response has not been processed, False otherwise.
        """
        if SharedClass.firstscreenshot and not SharedClass.processed:
            return True

    def action(self):
        """
        Defines the actions to be taken by the behavior.
        """
        SharedClass.processed = True
        self.robot.wait(0.1)
        print("----> control: Feedback")
        self.supress = False

        images = list(map(lambda x: {"image": x, "resize": 365}, load_image()))
        if SharedClass.img_counter == 0:
            base = "This line means this is a New Task DO NOT USE STORED INFORMATION from other last tasks\n\n" + f"""{robot_information} \n{general_description}  \n {phases} \n {rules()} \n {question} \n ***Feedback Data:***\n {SharedClass.sensor_data}"""
        else:
            base = f"""{robot_information} \n{general_description}  \n {phases} \n {rules()} \n {question} \n ***Feedback Data:***\n {SharedClass.sensor_data}"""

        print(SharedClass.sensor_data)
        promp_list = [base,]

        promp_list.extend(images)
        start = time.perf_counter()
        SharedClass.start_time = start
        response = generate_response(promp_list)
        SharedClass.response_counter += 1
        end = time.perf_counter()
        print(f"Response Time: {end - start:.2f} seconds")
        SharedClass.response = response

        promp_list.clear()