import json
import os
import re

import requests
from fuzzywuzzy import process

from pyclipper.clip.request import ClipRequestData
from pyclipper.config import Config
from pyclipper.timestamp import VideoTimestamp
from utils import find_items_starting_with
from google.protobuf.json_format import MessageToJson


def consecutive(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def re_in_list_search(strings, search_re) -> [str]:
    return list(filter(search_re.match, strings))[0] or -1


def youtube_url(title):
    import urllib.request
    from bs4 import BeautifulSoup

    query = urllib.parse.quote(title)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    urls = [
        (vid["title"], "https://www.youtube.com" + vid["href"])
        for vid in soup.findAll(attrs={"class": "yt-uix-tile-link"})
    ]

    match_dict = {u[1]: u[0] for u in urls}
    (expected_title, score, url) = process.extractOne(title, match_dict)

    if score < 95:
        raise Exception(
            f"Can't find a URL for a YouTube video with title {title}."
            f"\n\n"
            f"Closest match is {expected_title} with probability of {score}."
        )

    return url


def parse_youtube_screenshot_text(text) -> ClipRequestData:
    # [YOUTUBE]
    # this text is present in the screenshot if the user is holding the seekbar
    # and therefore indicates they are attempting to send start and end time
    # screenshot
    # [/YOUTUBE]
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

    # lol I just wanted to see if I could write this pythonically. Seems complicated though
    start_seconds, end_seconds = sorted(
        list(VideoTimestamp(ts).seconds for ts in relevant_timestamps_indices.values())
    )[0:2]

    # I believe YouTube Titles are limited to two lines. This helps in parsing the screenshot
    MAX_TITLE_LINES = 2
    # In the below screenshot, you can see that YouTube sometimes shows the location of a video
    # If it is shown, we need to ignore it, because it will throw off the YouTube URL search
    # https://i.imgur.com/NgQ0VVi.png
    POTENTIAL_LOCATION_OFFSET = 1
    last_timestamp_index = max(relevant_timestamps_indices.keys())
    youtube_title_range = slice(
        max(
            last_timestamp_index + POTENTIAL_LOCATION_OFFSET,
            views_line_index - MAX_TITLE_LINES,
        ),
        views_line_index,
    )

    youtube_title = " ".join(lines[youtube_title_range])
    url = youtube_url(youtube_title)
    return ClipRequestData(url, start_seconds, end_seconds)


def create_cache_path(image_uri):
    import base64

    screenshot_path = Config().screenshot_mount_point
    text_path = os.path.join(screenshot_path, "text")
    file_extension = ".txt"
    file_name = (
        f"{base64.b64encode(image_uri.encode()).decode('utf-8')}{file_extension}"
    )
    return os.path.join(text_path, file_name)


def write_to_cache(text, image_uri):
    path = create_cache_path(image_uri)
    with open(path, "w") as f:
        f.write(text)


def check_cache(image_uri):
    """Checks storage to see if we've already read this image. Avoids unnecessary Google Cloud Vision requests"""
    path = create_cache_path(image_uri)
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        return f.read()


def save_image_info(image_uri, info):
    screenshot_path = Config().screenshot_mount_point
    images_path = os.path.join(screenshot_path, "images")
    attributes_path = os.path.join(screenshot_path, "attributes")
    count = len(os.listdir(os.path.join(screenshot_path, images_path)))

    image_ext = ".png"
    image_name = f"{count:04d}{image_ext}"
    image_path = os.path.join(images_path, image_name)

    attributes_ext = ".json"
    attributes_name = f"{count:04d}{attributes_ext}"
    attribute_path = os.path.join(attributes_path, attributes_name)

    print(image_path)
    print(attribute_path)

    with open(image_path, "wb") as f:
        f.write(requests.get(image_uri).content)

    with open(attribute_path, "w") as f:
        f.write(MessageToJson(info))

    write_to_cache(info.full_text_annotation.text, image_uri)


def read_image(image_uri, skip_cache=False):
    if not skip_cache:
        text = check_cache(image_uri)
        if text:
            return text

    from google.cloud import vision
    from google.cloud.vision import types

    client = vision.ImageAnnotatorClient()

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

    print("hi")
    print(response)

    save_image_info(image_uri, response)
    return response.full_text_annotation.text


def parse_screenshot(image) -> ClipRequestData:
    if image is None:
        return ClipRequestData()
    print(f"Parsing {image}")
    text = read_image(image)
    return parse_youtube_screenshot_text(text)
