from pyclipper.clip.request import ClipRequest
from pyclipper.request import ClipperRequest
from .screenshot.parser import parse_screenshot
from .text.parser import parse_text
from ...config import Config

c = Config()


class MissingURLException(Exception):
    def __init__(self):
        self.message = """
        Could not figure out the URL of the video from your request.
        
        Please check our example and try again. Note that we can currently only read
        URLs from YouTube screenshots. For all other video sites, please share the
        URL directly with Clipper.
        
        Example: http://clipper.ngrok.io/
        """


def extract_url(image_request, text_request):
    if image_request.url:
        final_url = image_request.url
    elif text_request.url:
        final_url = text_request.url
    else:
        raise MissingURLException

    return final_url


def determine_timestamps(image_request, text_request):
    timestamps = [
        image_request.start_seconds,
        image_request.end_seconds,
        text_request.start_seconds,
        text_request.end_seconds,
    ]
    timestamps = [ts for ts in timestamps if ts]
    if len(timestamps) >= 2:
        start, end = timestamps[:2]
    elif len(timestamps) == 1:
        start = timestamps[0]
        end = start + c.default_clip_length
    else:
        start = 0
        end = c.default_clip_length
    return start, end


def merge_requests(image_request, text_request) -> ClipRequest:
    url = extract_url(image_request, text_request)
    start, end = determine_timestamps(image_request, text_request)

    return ClipRequest(url, start, end)


def parse_incoming_clipper_text_request(request: ClipperRequest) -> ClipRequest:
    image = request.image_url
    text = request.text

    image_clip_request = parse_screenshot(image)
    text_clip_request = parse_text(text)

    return merge_requests(image_clip_request, text_clip_request)
