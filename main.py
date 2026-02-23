


import time

from behaviour_mod.capture_data_bh import CaptureData
from behaviour_mod.feedback import Feedback
from behaviour_mod.process_response import ProcessResponse
from behaviour_mod.sharedclass import SharedClass
from config import Config
from roboboactions import RoboboActions


def main():
    """
        Main function to initialize and start the robot behaviors, and manage the execution flow.

        This function performs the following steps:
        1. Initializes the RoboboActions instance.
        2. Sets up shared parameters for behavior control.
        3. Creates instances of CaptureData, Feedback, and ProcessResponse behaviors.
        4. Starts the behavior threads.
        5. Keeps the main thread in a loop until the mission is marked as complete.
        6. Waits for all behavior threads to finish.
        7. Prints the total execution time and the number of responses generated.
        """

    config = Config(mode='simulation')  # Change to 'real' for real operation
    if config.is_simulation():
        SharedClass.simulation = True
    else:
        SharedClass.simulation = False
    robobo = RoboboActions(config)
    # Dictionary to be passed to behaviors to signal mission completion
    response = ""
    processed = 1
    params = {"stop": False, "response": response, "processed": processed}

    # Create behavior instances
    screenshot_behaviour = CaptureData(robobo, [], params,config)
    feedback_behaviour = Feedback(robobo, [], params)
    process_response_behaviour = ProcessResponse(robobo, [feedback_behaviour], params)
    # List of behavior threads
    threads = [screenshot_behaviour, feedback_behaviour, process_response_behaviour]
    SharedClass.start_time_ex  = time.perf_counter()
    # Start all behavior threads
    screenshot_behaviour.start()
    feedback_behaviour.start()
    process_response_behaviour.start()

    # Keep the main thread in a loop until the mission is marked as complete

    while not params["stop"]:
        time.sleep(0.1)
    end_time = time.perf_counter()
    print(f"Total Time: {end_time - SharedClass.start_time_ex:.2f} seconds \n {SharedClass.response_counter} responses generated")
    # Wait for all behavior threads to finish
    for thread in threads:
        thread.join()

    print("Fin de la misión")


if __name__ == "__main__":
    main()
