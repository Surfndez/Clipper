import argparse
import atexit
import os
import readline
import configparser

from pyclipper.config import Config

history_path = os.path.expanduser("~/.pyhistory")

def main(args):
    c = Config()
    pass
    # link = ytdl.download_and_trim(
    #     video_identifier="https://twitter.com/i/status/1246637822959693825", start="2s", end="5s",
    # )
    # print(link)




def save_history():
    import readline

    readline.write_history_file(os.path.expanduser("~/.pyhistory"))


def enable_history():
    if os.path.exists(history_path):
        readline.read_history_file(history_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    main(ap.parse_args())

    if os.path.exists(history_path):
        readline.read_history_file(history_path)

    atexit.register(save_history)
    # del os, atexit, readline, rlcompleter, save_history, history_path
