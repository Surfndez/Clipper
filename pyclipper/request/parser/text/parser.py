import re

from pyclipper.clip.request import ClipRequestData
from pyclipper.timestamp import VideoTimestamp


class RequestArgumentException(Exception):
    def __init__(self):
        super(RequestArgumentException, self).__init__(
            self, "We need a Video URL, a start time, and an end time."
        )


def pop_url(text):
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    try:
        i = regex.finditer(text)
        url = next(i)
        text = text.replace(url, "")
        return url, text
    except StopIteration:
        return None, text


def extract_timestamps(text):
    regex = re.compile(r"(?:(?:(\d+):)?(\d+):)(\d+)")
    timestamps = list(regex.finditer(text))

    if len(timestamps) >= 2:
        t1, t2 = timestamps[:2]
        return t1, t2

    if len(timestamps) == 1:
        return timestamps[0], None

    return None, None


def parse_text(text: str) -> ClipRequestData:
    video_url, text = pop_url(text)
    t1, t2 = extract_timestamps(text)
    start, end = (t1, t2) if t1 < t2 else (t2, t1)
    start, end = VideoTimestamp(start).seconds, VideoTimestamp(end).seconds
    return ClipRequestData(video_url, start, end)
