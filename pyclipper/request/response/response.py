from dataclasses import dataclass

from pyclipper.request import ClipperRequest


@dataclass
class ClipperResponse:

    request: ClipperRequest
    clip_url: str = None
    error: str = None
