import argparse
import atexit
import itertools
import os
import re
import readline
import subprocess
import cv2 as cv

import pytesseract
from PIL import Image
from cv2 import cv2

history_path = os.path.expanduser("~/.pyhistory")


def start_rabbitmq():
    start_rabbitmq_cmd = "docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management".split()
    subprocess.run(start_rabbitmq_cmd)


# Returns start time in seconds, end time in seconds and video url
def parse_youtube_screenshot_text(text):
    from fuzzywuzzy import process
    # this text is present in the screenshot if the user is holding the seekbar
    # and therefore indicates they are attempting to send start and end time
    # screenshot
    double_tap_text = 'Double tap left or right to skip 10 seconds'
    from pprint import pprint as pp
    lines = list(line for line in text.split('\n') if not re.match(r"\W", line) and line)
    # for i, line in enumerate(lines):
    #     print(f"{i}:\t{line}")

    match, percent = process.extractOne(double_tap_text, lines)
    two_timestamps_attempt = percent > 95

    timestamp_re = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d\d)")

    matches = list(re.finditer(timestamp_re, text))

    def first_match(needle):
        return [i for i, line in enumerate(lines) if line.startswith(needle)][0]

    ts_indices = dict((first_match(m.group()), m.group()) for m in matches)

    save_keys = []
    keys = list(ts_indices.keys())
    in_a_row = 3 if two_timestamps_attempt else 2
    for i in range(len(keys) - in_a_row):
        key_tuple = keys[i:i + in_a_row]
        # draw this out quit being so stubbord
        consecutive = True
        for j in range(len(key_tuple)):
            print("j: ", j)
            print("key: ", key_tuple[j])


        # if in_a_row == 2:
        #     k, k1 = keys[i:2]
        # else:
        #     k, k1, k2 = keys[i:i+3]
        #     print(k, k1, k2)
        #     if k2 - k1 == 1 and k1 - k == 1:
        #         save_keys.append(k)
        #         save_keys.append(k1)
        #         save_keys.append(k2)

    # ts_indices = {key: ts_indices[key] for key in save_keys}
    #
    # print("timestamps: ", ts_indices)
    #
    # last = max(ts_indices.keys())
    # potential_title_beginning = lines[last + 1]
    # print("title start: ", potential_title_beginning)


def black_white_image(image, out):
    if out is None:
        out = f"bw{image}"
    img = cv.imread(infile, 0)
    ret, thresh2 = cv.threshold(img, 238, 255, cv.THRESH_BINARY_INV)
    cv2.imwrite(outfile, thresh2)


def threshold():
    infile = "2.png"


    text = pytesseract.image_to_string(Image.open(outfile))
    return text
    # print(text)
    # titles = ['Original Image', 'BINARY_INV']
    # images = [img, thresh2]
    # for i in xrange(2):
    #     plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()

    # img = cv.imread(infile, 0)
    # ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    # ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
    # ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
    # ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
    # ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
    # titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    # images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    # for i in xrange(6):
    #     plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()


def main(args):
    text = threshold()
    parse_youtube_screenshot_text(text)
    pass
    # read_image()

    # read_image()

    # start_server()
    # start_rabbitmq()

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
