import os
import re

import requests
from fuzzywuzzy import process, fuzz
from google.protobuf.json_format import MessageToJson

from pyclipper.clip.request import ClipRequest
from pyclipper.config import Config
from pyclipper.timestamp import VideoTimestamp
from utils import find_items_starting_with, consecutive, cheat_youtube_url_lookup


def check_for_youtube_url(title_lines):
    print(title_lines)
    # first, check most obviously for full title
    url = youtube_url(" ".join(title_lines))
    print(url)

    # if the search did not work for both lines, we could have noise in the title
    # such as hashtags, location, etc. Try searching for just the second line,
    # which for YouTube videos will be directly above the watch count.
    if not url and len(title_lines) == 2:
        url = youtube_url(title_lines[1])
    return url


def youtube_url(title):
    """Searches YouTube by title for a video URL. Returns None if no good match is found."""

    print(title)
    cached = cheat_youtube_url_lookup(title)
    if cached:
        return cached

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
        return None

    return url


from pprint import pprint as p


def first_match_re(regex, lines):

    return [i for i, line in enumerate(lines) if re.search(regex, line)][0]


views_re = re.compile(r"\d*.* views")


def extract_youtube_title_lines_from_screenshot_text(screenshot_text_lines):
    views_line_index = first_match_re(views_re, screenshot_text_lines)

    youtube_title_range = slice(views_line_index - 2, views_line_index)

    youtube_title_lines = screenshot_text_lines[youtube_title_range]
    return youtube_title_lines


def parse_youtube_screenshot_text(text) -> ClipRequest:
    # [YOUTUBE]
    # this text is present in the screenshot if the user is holding the seekbar
    # and therefore indicates they are attempting to send start and end time
    # screenshot
    # [/YOUTUBE]
    double_tap_text = "Double tap left or right to skip 10 seconds"
    timestamp_re = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d\d)")

    lines = list(
        line for line in text.split("\n") if not re.match(r"\W", line) and line
    )

    views_line_index = first_match_re(views_re, lines)

    for i, line in enumerate(lines[:]):
        matches = list(re.finditer(timestamp_re, line))
        if len(matches) > 1:
            lines.pop(i)
            for j, m in enumerate(matches):
                lines.insert(i + j, m.group())

    (match, percent) = process.extractOne(double_tap_text, lines)

    two_timestamps_attempt = percent > 95

    matches = list(re.finditer(timestamp_re, text))

    # TODO pythonmebro
    all_ts_indices = dict()
    for m in matches:
        indices = find_items_starting_with(m.group(), lines)
        for i in indices:
            if i < views_line_index:
                # The only relevant timestamps appear above the "views" count in YouTube
                all_ts_indices[i] = m.group()

    save_keys = set()
    keys = list(all_ts_indices.keys())
    window_size = 3 if two_timestamps_attempt else 2
    for i in range(len(keys) - window_size + 1):
        window = keys[i : i + window_size]
        if consecutive(window):
            for k in window:
                save_keys.add(k)

    relevant_timestamps_indices = {key: all_ts_indices[key] for key in save_keys}
    relevant_timestamps = sorted(
        list(VideoTimestamp(ts).seconds for ts in relevant_timestamps_indices.values())
    )

    print(relevant_timestamps_indices)
    print(relevant_timestamps)

    if two_timestamps_attempt:
        start_seconds, end_seconds = relevant_timestamps[0:2]
    elif len(relevant_timestamps) >= 1:
        start_seconds = relevant_timestamps[0]
        end_seconds = None
    else:
        start_seconds, end_seconds = None, None

    youtube_title_lines = extract_youtube_title_lines_from_screenshot_text(lines)
    url = check_for_youtube_url(youtube_title_lines)
    return ClipRequest(url, start_seconds, end_seconds)


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
            print("cache hit")
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

    save_image_info(image_uri, response)
    return response.full_text_annotation.text


def parse_screenshot(image) -> ClipRequest:
    if image is None:
        return ClipRequest()
    text = read_image(image)
    return parse_youtube_screenshot_text(text)
