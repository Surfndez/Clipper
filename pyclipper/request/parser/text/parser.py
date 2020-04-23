from pyclipper.clip.request import ClipRequestData
from utils import first_url, extract_two_timestamp_seconds


class RequestArgumentException(Exception):
    def __init__(self):
        super(RequestArgumentException, self).__init__(
            self, "We need a Video URL, a start time, and an end time."
        )


def parse_text(text: str) -> ClipRequestData:
    if text is None:
        return ClipRequestData()
    video_url = first_url(text)
    t1, t2 = extract_two_timestamp_seconds(text)
    start, end = (t1, t2)
    return ClipRequestData(video_url, start, end)
