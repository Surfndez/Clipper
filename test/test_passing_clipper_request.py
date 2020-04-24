import unittest

from pyclipper.request import ClipperRequest


class TestEncodingDecodingClipperRequest(unittest.TestCase):
    def test_encode_decode_clipper_request(self):
        phone = "fake"
        image_url = "https://api.twilio.com/2010-04-01/Accounts/AC7cb1353ffd7b7ecb491ad68e2dd7461c/Messages/MM755dc09713851e848cee944386bd43b5/Media/MEb669920a3ef5fd367ab574d9131a4653"
        text = None

        r = ClipperRequest(phone=phone, image_url=image_url, text=text)

        self.assertEqual(r, ClipperRequest(request_json=r.json))


if __name__ == "__main__":
    unittest.main()
