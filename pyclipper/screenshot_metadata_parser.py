import io
import os
import re
from functools import cmp_to_key
from pprint import pprint as pp

import numpy as np
import pytesseract
import requests
from PIL import Image
from cv2 import cv2
from matplotlib import pyplot as plt

from pyclipper.screenshot_metadata import ScreenshotMetadata
from pprint import pprint as pp

from pyclipper.timestamp import VideoTimestamp
from utils import find_items_starting_with

SCREENSHOTS_DIRECTORY = "screenshots"


def show_plot(images):
    for i, (image, title) in enumerate(images):
        plt.subplot(1, len(images), i + 1), plt.imshow(image, "gray")
        plt.title(title)
        plt.xticks([]), plt.yticks([])
    plt.show()


def consecutive(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def re_in_list_search(strings, search_re):
    return list(filter(search_re.match, strings))[0] or -1


def top_half_image(image, out=None):
    if out is None:
        _, tail = os.path.split(image)
        out = os.path.join(SCREENSHOTS_DIRECTORY, f"top_{tail}")

    image = cv2.imread(os.path.join(SCREENSHOTS_DIRECTORY, image), 0)
    height, width = image.shape[:2]

    cropped_img = image[0 : height // 2, 0:width]

    cv2.imwrite(out, cropped_img)
    return out


def remove_noise(image, show=False):
    threshold = 248

    img = cv2.imread(image, 0)

    bw = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
    bwinv_orig = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)[1]
    bwinv = bwinv_orig.copy()

    contours, _ = cv2.findContours(bwinv_orig, 1, 2)
    bwcont, _ = cv2.findContours(bw, 1, 2)
    mask = np.ones(img.shape, np.uint8)
    mask2 = np.zeros(img.shape, np.uint8)

    def get_area(c1, c2):
        return cv2.contourArea(c2) - cv2.contourArea(c1)

    big_boxes = sorted(contours, key=cmp_to_key(get_area))[1:5]
    bigbw = sorted(bwcont, key=cmp_to_key(get_area))[0:5]

    for i, c in enumerate(bigbw):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(mask2, (x, y), (x + w, y + h), 255, 3)

    for i, c in enumerate(big_boxes):
        area = cv2.contourArea(c)
        if 5000 < area < 18000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 0, -1)

    cv2.bitwise_not(mask2, mask2)
    cv2.bitwise_and(mask2, bw, bw)
    cv2.bitwise_and(mask, bw, bw)
    kernel = np.ones((3, 3), np.uint8)
    bw = cv2.dilate(bw, kernel, iterations=1)
    bwcont, _ = cv2.findContours(bw, 1, 2)
    bigbw = sorted(bwcont, key=cmp_to_key(get_area))[0:3]
    mask = np.ones(img.shape, np.uint8)
    for i, c in enumerate(bigbw):
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 0, -1)
    cv2.bitwise_and(bw, mask, bw)
    cv2.bitwise_not(bw, bw)
    bw = cv2.GaussianBlur(bw, (5, 5), 1)

    _, tail = os.path.split(image)
    out = os.path.join(SCREENSHOTS_DIRECTORY, f"noise_removed_{tail}")
    cv2.imwrite(out, bw)

    if show:
        show_plot([(bw, "bw"), (mask2, "mask2"), (bwinv, "bwinv"), (mask, "mask")])

    return out


def youtube_url(title):
    import urllib.request
    from bs4 import BeautifulSoup

    query = urllib.parse.quote(title)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    # for vid in soup.findAll(attrs={"class": "yt-uix-tile-link"}):
    #     print(vid)

    urls = [
        "https://www.youtube.com" + vid["href"]
        for vid in soup.findAll(attrs={"class": "yt-uix-tile-link"})
        if vid["title"] == title
    ]
    return urls[0]


def parse_youtube_screenshot_text(text) -> ScreenshotMetadata:
    from fuzzywuzzy import process

    # [YOUTUBE]
    # this text is present in the screenshot if the user is holding the seekbar
    # and therefore indicates they are attempting to send start and end time
    # screenshot
    # [YOUTUBE]
    double_tap_text = "Double tap left or right to skip 10 seconds"
    timestamp_re = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d\d)")
    views_re = re.compile(r"\d*.* views")

    lines = list(
        line for line in text.split("\n") if not re.match(r"\W", line) and line
    )
    for i, line in enumerate(lines[:]):
        matches = list(re.finditer(timestamp_re, line))
        if len(matches) > 1:
            lines.pop(i)
            for j, m in enumerate(matches):
                lines.insert(i + j, m.group())

    (match, percent) = process.extractOne(double_tap_text, lines)

    two_timestamps_attempt = percent > 95

    matches = list(re.finditer(timestamp_re, text))

    def first_match_re(regex):
        return [i for i, line in enumerate(lines) if re.search(regex, line)][0]

    # TODO pythonmebro
    all_ts_indices = dict()
    for m in matches:
        indices = find_items_starting_with(m.group(), lines)
        for i in indices:
            all_ts_indices[i] = m.group()

    save_keys = set()
    keys = list(all_ts_indices.keys())
    window_size = 3 if two_timestamps_attempt else 2
    for i in range(len(keys) - window_size + 1):
        window = keys[i : i + window_size]
        if consecutive(window):
            for k in window:
                save_keys.add(k)

    views_line_index = first_match_re(views_re)

    relevant_timestamps_indices = {key: all_ts_indices[key] for key in save_keys}
    import q
    from pprint import pprint as pp

    # q.d()

    # lol I just wanted to see if I could write this pythonically. Seems complicated though
    start_seconds, end_seconds = sorted(
        list(VideoTimestamp(ts).seconds for ts in relevant_timestamps_indices.values())
    )[0:2]

    youtube_title_index = max(relevant_timestamps_indices.keys()) + 1

    youtube_title = " ".join(lines[youtube_title_index:views_line_index])

    url = youtube_url(youtube_title)

    return ScreenshotMetadata(url, start_seconds, end_seconds)


def invert_read(image):
    i = cv2.imread(image, 0)
    # inverted = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow("inverted", i)
    cv2.imwrite(image, i)
    text = pytesseract.image_to_string(Image.open(image))
    print(f"Raw Text from inverted image:\n\n{'-' * 30}{text}")


show = False

black_parsed = """
10:05 1
Search
Double tap left or right to skip 10 seconds
3:42:54
0:15
10:01:12 I:
Black Screen | A Screen Of Pure Black For 10 Hours | Blank |
Background | Backdrop | Screensaver |
298K views · 3 years ago
888
112
Share
Download
Save
Pictures of stuff for 10 hours
SUBSCRIBE
1.29K subscribers
Up next
Autoplay
4K Relaxing Fireplace with Crackling :
Fire Sounds - No Music - 4K UHD
- 2 Hours Screensaver
Balu - Relaxing Nature in 4K
9.1M views · 3 years ago
The Best
Relaxing
Fireplace
2:00:11
Ак)
3 hours of pure black screen!
CandRfun
309K views · 1 year ago
3:00:01
White Screen 10 Hours
Yukari Onosaki
3.4M views · 7 years ago
10:00:01
Deepest Sleep Music | Sleep Music
528HZ | Miracle Tone Healing |
Positive Energy Sleep | Delta Waves
Healing Sleep Tones
1.OIMI vIews months ago

"""


def read_image(image_uri):
    # return black_parsed

    from google.cloud import vision
    from google.cloud.vision import types

    client = vision.ImageAnnotatorClient()
    #
    # print(response)

    image = vision.types.Image()
    image.source.image_uri = image_uri
    response = client.text_detection(image=image)

    if (
        response.error
        and response.error.code == 7
        and "Please download the content and pass it in." in response.error.message
    ):
        image = types.Image(content=requests.get(image_uri).content)
        response = client.text_detection(image=image)

    pp(response)
    # for text in response.text_annotations:
    #     print("=" * 79)
    #     print(f'"{text.description}"')
    #     vertices = [f"({v.x},{v.y})" for v in text.bounding_poly.vertices]
    #     print(f'bounds: {",".join(vertices)}')
    return response.full_text_annotation.text

    #
    # TODO figure out if this works with other images
    # Instagram
    # Twitter
    # Vimeo
    # TikTok


class ScreenshotMetadataParser:
    def __init__(self, image):
        # TODO figure this out intelligently
        self.image = image
        self.downloaded = False

    def parse(self) -> ScreenshotMetadata:
        print(f"Parsing {self.image}")
        # invert_read(os.path.join(SCREENSHOTS_DIRECTORY, self.image))

        # self.downloaded = self.download_image_if_needed()

        # top = top_half_image(self.image)
        # ocr_ready = remove_noise(top, show)
        text = read_image(self.image)
        result = parse_youtube_screenshot_text(text)
        return result

    def download_image_if_needed(self):
        if not os.path.exists(os.path.join(SCREENSHOTS_DIRECTORY, self.image)):
            filename = "testing.png"
            # TODO use uuid filename
            # filename = str(uuid.uuid4()) + ".png"
            filepath = f"{SCREENSHOTS_DIRECTORY}/{filename}"
            with open(filepath, "wb") as f:
                f.write(requests.get(self.image).content)
                self.image = filename
            return True
        return False

    def clean_up_files(self, *images):
        if self.downloaded:
            os.remove(os.path.join(SCREENSHOTS_DIRECTORY, self.image))
        for image in images:
            if os.path.exists(image):
                os.remove(image)
            else:
                print(f"Why are you trying to remove {image}")
