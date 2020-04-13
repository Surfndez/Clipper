from dataclasses import dataclass

from pyclipper.screenshot_supported_service import ScreenshotSupportedService


@dataclass
class ScreenshotMetadata:
    # TODO: Come up with a better name for this as it is more broadly used than just in screenshots
    """Video screenshot metadata."""

    url: str
    start_seconds: int
    end_seconds: int
    service: ScreenshotSupportedService = ScreenshotSupportedService.YOUTUBE

    def __repr__(self):
        return f""" 
{self.url}
{self.start_seconds}
{self.end_seconds}
"""
