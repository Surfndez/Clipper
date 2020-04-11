from enum import Enum


class ScreenshotSupportedService(int, Enum):
    """
    Class for determining which video services I have verified work by sending a screenshot.
    """

    YOUTUBE = 1
