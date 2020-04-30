import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logfile = "pyclipper.log"
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')

handlers = (
	logging.FileHandler(logfile, mode="a"),
	logging.StreamHandler(sys.stdout)
)

for handler in handlers:
	handler.setFormatter(formatter)
	logger.addHandler(handler)
