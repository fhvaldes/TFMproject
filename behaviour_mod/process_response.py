
import ast

from behaviour_mod.behaviour import Behaviour
from behaviour_mod.sharedclass import SharedClass
from utils import delete_png_files


class ProcessResponse(Behaviour):
    """
    A class to process the response from the Robobo robot.

    Attributes:
        roboboactions (RoboboActions): Instance of the RoboboActions class to manage robot actions.
    """

    def __init__(self, robot, supress_list, params):
        """
        Initializes the ProcessResponse class.

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
            bool: True if the response is not empty and has been processed, False otherwise.
        """
        if SharedClass.response != "" and SharedClass.processed:
            return True

    def action(self):
        """
        Defines the actions to be taken by the behavior.
        """
        print("----> control: ProcessResponse")

        self.supress = False
        for bh in self.supress_list:
            bh.supress = True
        response = SharedClass.response

        # image = {
        #    "type": "image_url",
        #   "image_url": {
        #      "url": f"data:image/jpeg;base64,{load_image()}"
        # }}

        print(response)
        delete_png_files()
        taking_actions = ast.literal_eval(response)

        finish_bool = False

        for action in taking_actions:
            print(action)

            if action.startswith("turn") and "turn_tilt" not in action:
                if len(action.split()) == 3:
                    _, angle, direction = action.split()
                    self.roboboactions.actions["turn"](int(round(float(angle), 0)), direction)
            elif "turn_tilt" in action:
                _, angle = action.split()
                self.roboboactions.actions["turn_tilt"](int(round(float(angle), 0)))
            elif "finish" in action:
                finish_bool = True
                break
            elif action.startswith("wait"):
                _, time_value = action.split()
                self.roboboactions.actions["wait"](int(time_value))
            elif action.startswith("say"):
                text = action.replace("say", "")
                self.roboboactions.actions["say"](text)
            elif action.startswith("move_pan"):
                _, angle = action.split()
                self.roboboactions.actions["move_pan"](int(round(float(angle), 0)))
            elif action.startswith("move_forward"):
                self.roboboactions.actions["move_forward"]()
            elif action.startswith("move_backward"):
                self.roboboactions.actions["move_backward"]()
            elif action.startswith("continue"):
                self.roboboactions.actions["wait"](0.1)
            elif action in self.roboboactions.actions:
                self.roboboactions.actions[action]()
            else:
                print("Action not found")

        if finish_bool:
            self.roboboactions.actions["finish"]()
            self.params["stop"] = True

        SharedClass.response = ""
        SharedClass.processed = False

        self.supress = False

        # time.sleep(2)
        promp_list = []