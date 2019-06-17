import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
        Configure our logger
    """
    # Create logger object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Formatter creation to add time to the file
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # Handler creation to redirect logs into a file
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    # Config the handler
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # Add this handler to the logger
    logger.addHandler(file_handler)
    # An another handler for terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    return logger
