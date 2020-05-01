import os
import logging
from multiprocessing import Process

from pyclipper.environment_checker import check_environment_variables
from pyclipper.ngrok import start_ngrok
from pyclipper.server import start_server
from pyclipper.worker import start_worker

log = logging.getLogger(__name__)


def main():
    check_environment_variables()

    ngrok_process = Process(target=start_ngrok)
    worker_process = Process(target=start_worker)
    server_process = Process(target=start_server)

    ngrok_process.start()
    worker_process.start()
    server_process.start()

    ngrok_process.join()
    worker_process.join()
    server_process.join()


if __name__ == "__main__":
    main()
