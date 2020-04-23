import unittest

from utils import find_items_starting_with, first_url, extract_two_timestamp_seconds


class TestUtilities(unittest.TestCase):
    def test_lines_starting_with(self):
        matches = find_items_starting_with(
            "10:00:01", ["10:00:01", "10:00:01", "10:00:01", "10:00:04",]
        )
        self.assertEqual(matches, list(range(3)))

    def test_first_url(self):
        url = "http://youtube.com/foobar"
        s = f"blah {url}  https://google.com  https://yahoo.com"
        self.assertEqual(url, first_url(s))

    def test_extract_timestamps_seconds(self):
        s = "4:44 this should be ignored 3:33"
        expected = (284, 213)

        self.assertEqual(expected, extract_two_timestamp_seconds(s))

    def test_extract_timestamps_seconds_with_only_one_timestamp(self):
        s = "2:54"
        expected = (174, None)

        self.assertEqual(expected, extract_two_timestamp_seconds(s))


if __name__ == "__main__":
    unittest.main()
