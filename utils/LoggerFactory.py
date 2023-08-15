import logging
import sys


class LoggerFactory:
    """
        A Class that is responsible for logging throughout the application
        Ability to load to file, console and GUI Text Components
    """

    # A reference to the Logger that can be accessed anywhere in the application using the get_logger() method
    _LOG = None

    @staticmethod
    def __create_logger():
        """
            A private method that interacts with the python logging module
        """

        # Initialize the class variable with logger object
        LoggerFactory._LOG = logging.getLogger("Summative Assessment")
        LoggerFactory._LOG.setLevel(logging.INFO)

        # Create handlers
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler("app.log")

        # Create formatters and add it to handlers
        console_formatter = logging.Formatter("%(message)s")
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%d-%b-%y %H:%M:%S")
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        LoggerFactory._LOG.addHandler(console_handler)
        LoggerFactory._LOG.addHandler(file_handler)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger():
        """
            A static method called by other modules to initialize logger in their own module.
            Using the Singleton Pattern.
        """

        # Checks to see if a _LOG has already been created and if so returns the existing log
        # otherwise will instantiate a new one
        if LoggerFactory._LOG is None:
            LoggerFactory._LOG = LoggerFactory.__create_logger()
        return LoggerFactory._LOG
