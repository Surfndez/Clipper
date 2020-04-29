from pyclipper.clip.request import ClipRequest
from pyclipper.utils import first_url, extract_two_timestamp_seconds


class RequestArgumentException(Exception):
    def __init__(self):
        super(RequestArgumentException, self).__init__(
            self, "We need a Video URL, a start time, and an end time."
        )


def parse_text(text: str) -> ClipRequest:
    if text is None:
        return ClipRequest()
    video_url = first_url(text)
    t1, t2 = extract_two_timestamp_seconds(text)
    start, end = (t1, t2)
    return ClipRequest(video_url, start, end)
