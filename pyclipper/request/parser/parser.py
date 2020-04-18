from dataclasses import astuple

from pyclipper.clip.request import ClipRequestData
from pyclipper.request import ClipperServerRequestData
from .screenshot.parser import parse_screenshot
from .text.parser import parse_text


def merge_requests(image_request, text_request) -> ClipRequestData:
    # figure out which vars to pick
    pass


def parse_incoming_clipper_text_request(
    request: ClipperServerRequestData,
) -> ClipRequestData:
    image = request.image_url
    image_clip_request, text_clip_request = None, None
    if image is not None:
        image_clip_request = parse_screenshot(image)

    text_clip_request = parse_text(request.text)

    return merge_requests(image_clip_request, text_clip_request)
