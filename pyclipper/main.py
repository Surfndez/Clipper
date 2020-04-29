from pyclipper.worker import start_worker
from pyclipper.server import start_server
import multiprocessing
import signal
import os


def check_env_vars():
    # Check Google Cloud Vision credentials
    pass


def main():
    # check environment vars
    check_env_vars()

    # start worker
    p = multiprocessing.Process(target=start_worker)
    p.start()

    # start server
    p2 = multiprocessing.Process(target=start_server)
    p2.start()

    p.join()
    p2.join()


if __name__ == "__main__":
    main()
