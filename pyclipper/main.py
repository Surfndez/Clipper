from multiprocessing import Process

from pyclipper.config.config import log_config
from pyclipper.environment_checker import check_environment_variables
from pyclipper.ngrok import start_ngrok
from pyclipper.server import start_server
from pyclipper.worker import start_worker


def main():
    log_config()
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
