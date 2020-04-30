import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logfile = "pyclipper.log"
file_handler = logging.FileHandler(logfile, mode="a")
stream_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
