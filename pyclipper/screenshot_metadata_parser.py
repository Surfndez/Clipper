import re
from pprint import pprint as pp
from fuzzywuzzy import process

import requests

from pyclipper.screenshot_metadata import ScreenshotMetadata
from pyclipper.timestamp import VideoTimestamp
from utils import find_items_starting_with


def consecutive(nums):
    return sorted(nums) == list(range(min(nums), max(nums) + 1))


def re_in_list_search(strings, search_re):
    return list(filter(search_re.match, strings))[0] or -1


def youtube_url(title):

    import urllib.request
    from bs4 import BeautifulSoup

    query = urllib.parse.quote(title)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    urlss = [
        (vid["title"], "https://www.youtube.com" + vid["href"])
        for vid in soup.findAll(attrs={"class": "yt-uix-tile-link"})
    ]

    match_dict = {u[1]: u[0] for u in urlss}
    (title, score, url) = process.extractOne(title, match_dict)

    if score < 95:
        raise Exception(
            f"Can't find a URL for a YouTube video with title {title}.\n\nClosest match is {match} with probability of {percent}."
        )

    return url


def parse_youtube_screenshot_text(text) -> ScreenshotMetadata:
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

    # q.d()

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
    return ScreenshotMetadata(url, start_seconds, end_seconds)


def read_image(image_uri):

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
        self.image = image
        self.downloaded = False

    def parse(self) -> ScreenshotMetadata:
        print(f"Parsing {self.image}")
        text = read_image(self.image)
        result = parse_youtube_screenshot_text(text)
        return result
