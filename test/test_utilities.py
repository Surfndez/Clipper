import unittest

from pyclipper.screenshot_metadata_parser import parse_youtube_screenshot_text
from utils import find_items_starting_with


class TestUtilites(unittest.TestCase):
    def test_lines_starting_with(self):
        matches = find_items_starting_with(
            "10:00:01", ["10:00:01", "10:00:01", "10:00:01", "10:00:04",]
        )
        self.assertEqual(matches, list(range(3)))


if __name__ == "__main__":
    unittest.main()
