from dataclasses import dataclass

from pyclipper.config import ScreenshotSupportedService


@dataclass
class ClipRequestData:
    """Data specifying a clip from a video."""

    url: str = None
    start_seconds: int = None
    end_seconds: int = None
    service: ScreenshotSupportedService = ScreenshotSupportedService.YOUTUBE

    def __repr__(self):
        return f"""{self.url}    
                   {self.start_seconds}    
                   {self.end_seconds}"""
