import os
import logging
from multiprocessing import Process

from pyclipper.server import start_server
from pyclipper.worker import start_worker

log = logging.getLogger(__name__)


def check_env_vars():
    key_path = "/tmp/keys/key.json"
    with open(key_path) as k:
        log.debug(k.readlines())

    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    log.debug(os.environ)
    log.debug(creds)

    google_credentials_missing = creds is None or len(creds) == 0
    if google_credentials_missing:
        raise Exception(
            """
In order to use Clipper, please open the .env file in the root of the project and tell it where you downloaded your Google Cloud Platform key.json.

If you don't have a key for Google Cloud Vision, please go here, follow the instructions, and then tell the .env file where you downloaded the key: 

https://cloud.google.com/vision/docs/quickstart-client-libraries

"""
        )


def main():
    # check environment vars
    check_env_vars()

    worker_process = Process(target=start_worker)
    server_process = Process(target=start_server)

    worker_process.start()
    server_process.start()

    worker_process.join()
    server_process.join()


if __name__ == "__main__":
    main()
