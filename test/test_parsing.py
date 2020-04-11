import unittest

from pyclipper.screenshot_metadata import ScreenshotMetadata
from pyclipper.screenshot_metadata_parser import parse_youtube_screenshot_text
from pyclipper.timestamp import VideoTimestamp


class TestParsing(unittest.TestCase):
    def test_parse_read_youtube_text(self):
        expected = ScreenshotMetadata(
            "https://www.youtube.com/watch?v=J3pF2jkQ4vc",
            VideoTimestamp("4:59:28").seconds,
            VideoTimestamp("10:00:00").seconds,
        )
        failing_bw = "4:41 1\nDouble tap left or right to skip 10 seconds\n4:59:28\n10:00:00\n10:00:00\nWhite Screen 10 Hours\n3.3M views \302\267 7 years ago\n13K\n1.5K\nShare\nDownload\nSave\nYukari Onosaki\n2.53K subscribers\nSUBSCRIBE\nUp next\nAutoplay\nWhite Screen - 1 hour 1080p\nDenis Productions\n150K views \302\267 3 years ago\n1:00:01\nWhite Screen 1 hour - Pantalla\nBlanca 1 hora | FULL HD 1080p T\nChannel Special Subscribers\n140K views \302\267 2 years ago\n1:00:01\nDeepest Sleep Music | Sleep Music\n528HZ | Miracle Tone Healing l\nPositive Energy Sleep | Delta Waves\nHealing Sleep Tones\nRecommended for you\n10:10:18\nSCN\nZoom Surprise: Some Good News\nwith John Krasinski Ep. 2\nSomeGoodNews\nRecommended for you\n"

        actual = parse_youtube_screenshot_text(failing_bw)
        self.assertEqual(
            expected, actual,
        )


if __name__ == "__main__":
    unittest.main()
