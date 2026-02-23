import os

from robobopy_videostream.RoboboVideo import RoboboVideo


class SharedClass:
    """
    A class to manage shared states and actions for the Robobo robot.

    Attributes:
        firstscreenshot (bool): Indicates if the first screenshot has been taken.
        response (str): Stores the response from the robot.
        processed (bool): Indicates if the response has been processed.
        firstfeedback (bool): Indicates if the first feedback has been received.
        sensor_data (list): Stores sensor data from the robot.
        img_counter (int): Counter for the number of images taken.
        start_time (int): Start time for the session.
        response_counter (int): Counter for the number of responses received.
        videoStream (RoboboVideo): Instance of the RoboboVideo class to manage video streaming.
    """

    firstscreenshot = False
    response = ""
    processed = False
    firstfeedback = False
    sensor_data = []
    img_counter = 0
    start_time = 0
    response_counter = 0
    simulation = True



    @staticmethod
    def init_main_if_needed():
        if SharedClass.simulation is False:
            import main
            videoStream = RoboboVideo(os.getenv("ROBOT_IP"))
            videoStream.connect()
