import unittest
from dataclasses import asdict

from pyclipper.clip.request import ClipRequest
from pyclipper.config.config import default_clip_length
from pyclipper.request import ClipperRequest
from pyclipper.request.parser.parser import parse_incoming_clipper_text_request


class TestClipperServerRequests(unittest.TestCase):
    """
    Tests that a text message request is converted to information that can then be used to download and split the clip

    """

    def test_image_with_three_timestamps(self):
        # arrange
        three_timestamp_screenshot = "https://i.imgur.com/NilxzJP.png"
        three_timestamp_url = "https://www.youtube.com/watch?v=J3pF2jkQ4vc"
        three_timestamp_text = None
        three_timestamp_t1_seconds = 13092
        three_timestamp_t2_seconds = 16364

        request = ClipperRequest(
            "phone", three_timestamp_screenshot, three_timestamp_text
        )

        expected = ClipRequest(
            three_timestamp_url, three_timestamp_t1_seconds, three_timestamp_t2_seconds,
        )

        # act
        actual = parse_incoming_clipper_text_request(request)

        # assert
        self.assertEqual(asdict(expected), asdict(actual))

    def test_image_with_three_timestamps_with_text(self):
        # arrange
        three_timestamp_screenshot = "https://i.imgur.com/NilxzJP.png"
        three_timestamp_url = "https://www.youtube.com/watch?v=J3pF2jkQ4vc"
        three_timestamp_text = "4:44 this should be ignored 3:33"
        three_timestamp_t1_seconds = 13092
        three_timestamp_t2_seconds = 16364

        request = ClipperRequest(
            "phone", three_timestamp_screenshot, three_timestamp_text
        )

        expected = ClipRequest(
            three_timestamp_url, three_timestamp_t1_seconds, three_timestamp_t2_seconds,
        )

        # act
        actual = parse_incoming_clipper_text_request(request)

        # assert
        self.assertEqual(asdict(expected), asdict(actual))

    def test_image_with_two_timestamps_with_text(self):
        # arrange
        two_timestamp_screenshot = "https://i.imgur.com/9bpBzMp.jpg"
        two_timestamp_url = "https://www.youtube.com/watch?v=3OP-q55hOUI"
        two_timestamp_text = "2:54"
        two_timestamp_t1_seconds = 134
        two_timestamp_t2_seconds = 174

        request = ClipperRequest("phone", two_timestamp_screenshot, two_timestamp_text)

        expected = ClipRequest(
            two_timestamp_url, two_timestamp_t1_seconds, two_timestamp_t2_seconds,
        )

        # act
        actual = parse_incoming_clipper_text_request(request)

        # assert
        self.assertEqual(asdict(expected), asdict(actual))

    # test.test_parse_clipper_request.TestClipperServerRequests.test_image_with_two_timestamps_with_no_text_uses_default_clip_length
    def test_image_with_two_timestamps_with_no_text_uses_default_clip_length(self):
        # arrange
        two_timestamp_screenshot = "https://i.imgur.com/9bpBzMp.jpg"
        two_timestamp_url = "https://www.youtube.com/watch?v=3OP-q55hOUI"
        two_timestamp_text = None
        two_timestamp_t1_seconds = 134
        two_timestamp_t2_seconds = 144

        request = ClipperRequest("phone", two_timestamp_screenshot, two_timestamp_text)

        expected = ClipRequest(
            two_timestamp_url, two_timestamp_t1_seconds, two_timestamp_t2_seconds,
        )

        # act
        actual = parse_incoming_clipper_text_request(request)

        # assert
        self.assertEqual(asdict(expected), asdict(actual))

    def test_image_with_no_timestamps_defaults_to_0_to_10_seconds(self):
        # arrange
        no_timestamp_screenshot = "https://i.imgur.com/3i85i3a.png"
        no_timestamp_url = "https://www.youtube.com/watch?v=8mBmZDF23Lc"
        no_timestamp_text = None
        no_timestamp_t1_seconds = 0
        no_timestamp_t2_seconds = default_clip_length

        request = ClipperRequest("phone", no_timestamp_screenshot, no_timestamp_text)

        expected = ClipRequest(
            no_timestamp_url, no_timestamp_t1_seconds, no_timestamp_t2_seconds,
        )

        # act
        actual = parse_incoming_clipper_text_request(request)

        # assert
        self.assertEqual(asdict(expected), asdict(actual))
