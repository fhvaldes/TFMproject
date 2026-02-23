# config.py
class Config:
    def __init__(self, mode='real'):
        """
        Initializes the configuration.

        Args:
            mode (str): Mode of operation, either 'real' or 'simulation'. Default is 'real'.
        """
        self.mode = mode

    def is_simulation(self):
        """
        Checks if the mode is set to simulation.

        Returns:
            bool: True if mode is 'simulation', False otherwise.
        """
        return self.mode == 'simulation'