from dataclasses import dataclass

from pyclipper.config import ScreenshotSupportedService


@dataclass
class ClipRequestData:
    """Data specifying a clip from a video."""

    url: str = None
    start_seconds: int = None
    end_seconds: int = None
    service: ScreenshotSupportedService = ScreenshotSupportedService.YOUTUBE
