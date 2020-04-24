import unittest

from pyclipper.request.parser.screenshot.parser import (
    extract_youtube_title_lines_from_screenshot_text,
)


class TestParsing(unittest.TestCase):
    # nodemon -e py --exec "python -m unittest test.test_parsing_screenshot.TestParsing.test_parse_youtube_potential_title_lines_from_screenshot_text"
    def test_parse_youtube_potential_title_lines_from_screenshot_text(self):
        screenshot_text = """5:31 1
A SSrapp
O localhost 3000
Apps
Otheookmarks
ssi-app
My nuxt app on Cloud Run & Firebase
Documentation
GitHub
2:14 / 7:50
#cloudrun #docker #serverless
Cloud Run QuickStart - Docker to Serverless
40,915 views ·1 year ago
1.7K
19
Share
Download
Save
Fireship
SUBSCRIBED N
326K subscribers
Published on Apr 10, 2019
Use the brand new Cloud Run service to turn any Docker image into
a serverless microservice on Google Cloud Platform. In this demo, we
dockerize and deploy a server-rendered Nuxt/Vue app to Firebase
Hosting https://fireship.io/lessons/firebase-...
Cloud Run https://cloud.google.com/run/
Nuxt https://nuxtjs.org/
Firebase Microservices https://firebase.google.com/docs/host...
#cloudrun #docker #serverless
Category
Science & Technology
Buy Fireship merchandise
From Teespring
TATI
fireship io
fireship.io
$19.00
$44.99
$18.99
""".split(
            "\n"
        )
        actual = extract_youtube_title_lines_from_screenshot_text(screenshot_text)
        expected = [
            "#cloudrun #docker #serverless",
            "Cloud Run QuickStart - Docker to Serverless",
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
