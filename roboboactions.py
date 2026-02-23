import os

from robobopy.Robobo import Robobo
from robobopy.utils.IR import IR


class RoboboActions:
    """
    Class to manage actions for the Robobo robot.
    """

    def __init__(self, config):
        """
                Initializes the RoboboActions class.

                - Connects to the Robobo robot.
                - Starts the video stream.
                - Moves the tilt and pan to initial positions.
                - Stores the initial orientation.
                - Defines a dictionary of available actions.
        """
        self.config = config
        if self.config.is_simulation():
            self.robobo = Robobo("localhost")  # for simulation
        else:
            self.robobo = Robobo(os.getenv("ROBOT_IP"))  # for real

        self.robobo.connect()
        # Add a delay to allow the orientation sensor to stabilize
        self.robobo.wait(5)  # Wait for 2 seconds
        if not self.config.is_simulation():
            self.robobo.startStream()
        self.robobo.moveTiltTo(110, 30, False)
        self.robobo.movePanTo(0, 30, True)
        self.start_orientation = int(self.robobo.readOrientationSensor().yaw)  # Store initial orientation
        self.actions = {
            "move_forward": self._move_forward,
            "move_backward": self._move_backward,
            "turn": self._turn,
            "stop": self.robobo.stopMotors,
            "wait": self.robobo.wait,
            "turn_tilt": self._move_tilt,
            "say": self._sayText,
            "move_pan": self._movePanTo,
            "continue": self.robobo.wait(0.1),
            "finish": self._finish
        }

    def get_actions(self):
        """
        Returns the available actions.

        Returns:
            dict_keys: Keys of the actions dictionary.
        """
        return self.actions.keys()  # Return the class variable

    def wait(self, time):
        """
        Waits for a specified amount of time.

        Args:
            time (float): Time to wait in seconds.
        """
        self.robobo.wait(time)

    def _move_wheels(self, left_speed, right_speed):
        """
        Moves the wheels of the Robobo robot.

        Args:
            left_speed (int): Speed of the left wheel.
            right_speed (int): Speed of the right wheel.
        """
        self.robobo.moveWheels(left_speed, right_speed)
        self.robobo.wait(0.1)

    def _move_tilt(self, angle):
        """
        Moves the tilt of the Robobo robot.

        Args:
            angle (int): Angle to move the tilt to.
        """
        self.robobo.moveTiltTo(angle, 30, False)

    def _move_forward(self):
        """
        Moves the Robobo robot forward.
        """
        self.robobo.moveWheels(10, 10)

    def _move_backward(self):
        """
        Moves the Robobo robot backward.
        """
        self.robobo.moveWheels(-10, -10)

    def _turn(self, angle=90, direction="right"):
        """
        Performs a turn of the specified angle (degrees) in the given direction.

        Args:
            angle (int): Angle to turn in degrees. Default is 90.
            direction (str): Direction to turn ('right' or 'left'). Default is 'right'.

        Raises:
            ValueError: If the direction is not 'right' or 'left'.
        """

        if direction.lower() not in ("right", "left"):
            raise ValueError("Invalid direction. Must be 'right' or 'left'.")

        self.start_orientation = self.robobo.readOrientationSensor().yaw

        turn_speed = 15
        if direction == "left":
            target_orientation = (self.start_orientation - angle) % 360
            self.robobo.moveWheels(0, turn_speed)
        else:  # direction == "left"
            target_orientation = (self.start_orientation + angle) % 360
            self.robobo.moveWheels(turn_speed, 0)

        while True:
            current_orientation = self.robobo.readOrientationSensor().yaw

            # Check if the current orientation is within a 5 degree margin of the target orientation
            if abs((current_orientation - target_orientation + 360) % 360) <= 10:
                break

            self.robobo.wait(0.1)

        self.robobo.stopMotors()
        self.start_orientation = self.robobo.readOrientationSensor().yaw

    # print(f"End Orientation: {self.start_orientation}")

    def read_sensors(self):
        """
        Reads the sensor values from the Robobo robot.

        Returns:
            dict: Dictionary containing IR sensor values and camera orientation yaw angle.
        """
        # print(self.robobo.readWheelPosition(wheel=Wheels.R))
        return {"IR Sensor Values":
                    {"IRFrontC": self.robobo.readIRSensor(IR.FrontC),
                     "IRFrontR": self.robobo.readIRSensor(IR.FrontR),
                     "IRFrontL": self.robobo.readIRSensor(IR.FrontL)},
                "Camera Orientation Yaw Angle in degrees": self.robobo.readOrientationSensor().yaw
                }

    def _sayText(self, text):
        """
        Makes the Robobo robot say the specified text.

        Args:
            text (str): Text to be spoken by the robot.
        """
        self.robobo.sayText(text, wait=False)

    def _finish(self):
        """
        Stops the motors and disconnects the Robobo robot.
        """
        self.robobo.stopMotors()
        self.robobo.disconnect()

    def _movePanTo(self, angle):
        """
        Moves the pan of the Robobo robot to the specified angle.

        Args:
            angle (int): Angle to move the pan to.
        """
        self.robobo.movePanTo(angle, 10, True)
