import unittest

from pyclipper.clip.request import ClipRequestData
from pyclipper.request import ClipperServerRequestData
from pyclipper.request.parser.parser import parse_incoming_clipper_text_request

THREE_TIMESTAMP_SCREENSHOT = "https://i.imgur.com/NilxzJP.png"
THREE_TIMESTAMP_URL = "https://www.youtube.com/watch?v=J3pF2jkQ4vc"
THREE_TIMESTAMP_TEXT = None
THREE_TIMESTAMP_T1_SECONDS = 13092
THREE_TIMESTAMP_T2_SECONDS = 16364


TWO_TIMESTAMP_SCREENSHOT = "https://i.imgur.com/9bpBzMp.jpg"
TWO_TIMESTAMP_URL = "https://www.youtube.com/watch?v=3OP-q55hOUI"
TWO_TIMESTAMP_TEXT = 174
TWO_TIMESTAMP_T1_SECONDS = 134
TWO_TIMESTAMP_T2_SECONDS = 174


TWO_TIMESTAMP_BEFORE_SCREENSHOT = "https://i.imgur.com/9bpBzMp.jpg"
TWO_TIMESTAMP_BEFORE_URL = "https://www.youtube.com/watch?v=3OP-q55hOUI"
TWO_TIMESTAMP_BEFORE_TEXT = 114
TWO_TIMESTAMP_BEFORE_T1_SECONDS = 134
TWO_TIMESTAMP_BEFORE_T2_SECONDS = 114

# TODO backwards video if user is an idiot


class TestClipperServerRequests(unittest.TestCase):
    """
    Tests that a text message request is converted to information that can then be used to download and split the clip

    """

    def test_incoming_requests_happy_path_parsed_correctly(self):
        # arrange
        request_result_pairs = [
            (
                ClipperServerRequestData(
                    "phone", THREE_TIMESTAMP_SCREENSHOT, THREE_TIMESTAMP_TEXT
                ),
                ClipRequestData(
                    THREE_TIMESTAMP_URL,
                    THREE_TIMESTAMP_T1_SECONDS,
                    THREE_TIMESTAMP_T2_SECONDS,
                ),
            ),
            (
                ClipperServerRequestData(
                    "phone", TWO_TIMESTAMP_SCREENSHOT, TWO_TIMESTAMP_TEXT
                ),
                ClipRequestData(
                    TWO_TIMESTAMP_URL,
                    TWO_TIMESTAMP_T1_SECONDS,
                    TWO_TIMESTAMP_T2_SECONDS,
                ),
            ),
        ]

        # act
        for request, data in request_result_pairs:
            actual = parse_incoming_clipper_text_request(request)
            expected = data

            # assert
            self.assertEqual(expected, actual)
