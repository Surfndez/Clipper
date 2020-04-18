import unittest

from dotmap import DotMap as d

from pyclipper.clip.request import ClipRequestData
from pyclipper.request.parser.screenshot.parser import parse_screenshot

fails = [
    d(
        image="https://s3-external-1.amazonaws.com/media.twiliocdn.com/AC7cb1353ffd7b7ecb491ad68e2dd7461c/229fc07e5db0dac9d865125a9d1651bb",
        text="12:19 9\nDouble tap left or right to skip 10 seconds\n4:44\n0:04\n11:32\nO CAMBODIA\nGordon Ramsay Cooks Buffalo For A Cambodian Tribe | Gordon's\nGreat Escape\n13M views 1 year ago\n155K\n5.3K\nShare\nDownload\nSave\nGordon Ramsay\nSUBSCRIBE\n13.7M subscribers\nUp next\nAutoplay\nGordon Ramsay Cooks For\nCambodian Royalty | Gordon's Great\nEscape\nGordon Ramsay\n4.2M views 1 year ago\nGORDON\nRAMSAY\n7:59\nGordon Ramsay Shows How To\nMake A Lamb Chop Dish At Home |\nRamsay in 10\nGordon Ramsay\nRecommended for you\nRAMSAY\n1543\nGORDON\nRAMSAY\nEating with the World's Most\nIsolated Tribell! The Tree People of\nPapua, Indonesial!\nBest Ever Food Review Show\n11M views 7 months ago\n13:03\nCatching Wild Catfish By Hand in\nOklahoma - Gordon Ramsay\n",
        url="https://www.youtube.com/watch?v=iXwfBJYCTc4",
        expected_start=4,
        expected_end=284,
    )
]


class TestParsing(unittest.TestCase):
    @unittest.skip
    def test_parse_youtube_screen_contents(self):
        for fail in fails:
            expected = ClipRequestData(
                fail.url, fail.expected_start, fail.expected_end,
            )

            actual = parse_screenshot(fails[0].text)
            self.assertEqual(
                expected, actual,
            )


if __name__ == "__main__":
    unittest.main()
