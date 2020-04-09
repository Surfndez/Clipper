import argparse
import atexit
import os
import re
import readline
import subprocess

import numpy as np
import pytesseract
from PIL import Image
from cv2 import cv2
from matplotlib import pyplot as plt
from pprint import pprint as pp
from past.builtins import xrange

history_path = os.path.expanduser("~/.pyhistory")


def start_rabbitmq():
    start_rabbitmq_cmd = "docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management".split()
    subprocess.run(start_rabbitmq_cmd)


def consecutive(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def re_in_list_search(strings, search_re):
    return list(filter(search_re.match, strings))[0] or -1


# Returns start time in seconds, end time in seconds and video url
def parse_youtube_screenshot_text(text):
    print(text)
    from fuzzywuzzy import process
    # [YOUTUBE]
    # this text is present in the screenshot if the user is holding the seekbar
    # and therefore indicates they are attempting to send start and end time
    # screenshot
    # [YOUTUBE]
    double_tap_text = 'Double tap left or right to skip 10 seconds'
    timestamp_re = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d\d)")

    lines = list(line for line in text.split('\n') if not re.match(r"\W", line) and line)
    for i, line in enumerate(lines[:]):
        matches = list(re.finditer(timestamp_re, line))
        if len(matches) > 1:
            lines.pop(i)
            for j, m in enumerate(matches):
                lines.insert(i + j, m.group())

    pp(lines)


    match, percent = process.extractOne(double_tap_text, lines)
    two_timestamps_attempt = percent > 95

    matches = list(re.finditer(timestamp_re, text))

    def first_match(needle):
        print(needle)
        return [i for i, line in enumerate(lines) if line.startswith(needle)][0]

    all_ts_indices = dict((first_match(m.group()), m.group()) for m in matches)
    print(all_ts_indices)

    save_keys = set()
    keys = list(all_ts_indices.keys())
    window_size = 3 if two_timestamps_attempt else 2
    print(window_size)
    for i in range(len(keys) - window_size + 1):
        window = keys[i:i+window_size]
        print(window)
        if consecutive(window):
            for k in window:
                save_keys.add(k)

    relevant_timestamps_indices = {key: all_ts_indices[key] for key in save_keys}

    print("timestamps: ", relevant_timestamps_indices)




    #
    # last = max(ts_indices.keys())
    # potential_title_beginning = lines[last + 1]
    # print("title start: ", potential_title_beginning)
    # TODO figure out if this works with other images
    # Instagram
    # Twitter
    # Vimeo
    # TikTok
    return "parsed youtube? screenshot"


def black_white_image(image, out=None):
    def show(img):
        plt.imshow(img, cmap="gray")
        plt.show()
    threshold_value = 235
    if out is None:
        out = f"bw{image}"

    # if os.path.exists(out):
    #     return out
    img = cv2.imread(image, 0)
    ret, thresh2 = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY_INV)
    show(thresh2)

    kernel = np.ones((3, 3), np.uint8)
    img = cv2.erode(thresh2, kernel, iterations=1)
    # show(img)


    #
    cv2.imwrite(out, thresh2)
    return out


def top_half_image(image, out=None):
    if out is None:
        out = f"top_{image}"

    # if os.path.exists(out):
    #     return out

    image = cv2.imread(image, 0)
    height, width = image.shape[:2]

    cropped_img = image[0:height // 2, 0:width]

    # cv.waitKey(0)
    # cv.destroyAllWindows()
    cv2.imwrite(out, cropped_img)
    return out

# https://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv
def business_card():
    ww = "ww.png"
    img = cv2.imread(ww)
    img = cv2.resize(img,(400,500))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray = cv2.threshold(gray,127,255,0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape,np.uint8)

    contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if 200<cv2.contourArea(cnt)<5000:
            cv2.drawContours(img,[cnt],0,(0,255,0),2)
            cv2.drawContours(mask,[cnt],0,255,-1)

    cv2.bitwise_not(gray2, gray2, mask)

    cv2.imshow('IMG', gray2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def _main():
    ww = "ww.png"
    one = "1.jpg"
    two = "2.jpg"
    tjbox = "tj_box.jpeg"
    tjnobox = "tj_no_box.jpeg"
    infile = ww
    print(f"evalutating: {infile}")
    out = black_white_image(infile)
    out = top_half_image(out)
    text = pytesseract.image_to_string(Image.open(tjbox))
    # if os.path.exists(out):
    #     os.remove(out)
    parsed = parse_youtube_screenshot_text(text)
    print(parsed)
    # start_server()
    # start_rabbitmq()

    # link = ytdl.download_and_trim(
    #     video_identifier="https://twitter.com/i/status/1246637822959693825", start="2s", end="5s",
    # )
    # print(link)


def bullshit():



def main(args):
    _main()
    # bullshit()


def save_history():
    import readline

    readline.write_history_file(os.path.expanduser("~/.pyhistory"))


def enable_history():
    if os.path.exists(history_path):
        readline.read_history_file(history_path)


def demo_threshold(infile):
    img = cv2.imread(infile, 0)
    ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
    titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in xrange(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    main(ap.parse_args())

    if os.path.exists(history_path):
        readline.read_history_file(history_path)

    atexit.register(save_history)
