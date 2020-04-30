import unittest
import time
import logging

log = logging.getLogger(__name__)

videos = "pyclipper/assets"
full_video_path_prefix = f"{videos}/full"
youtube_id = "iXwfBJYCTc4"
full_video_path = f"{full_video_path_prefix}/{youtube_id}.mp4"


class TestVideoTrimSpeed(unittest.TestCase):
    @unittest.skip
    def test_video_trim_speed(self):
        tic = time.perf_counter()
        start = 4
        end = 284
        toc = time.perf_counter()
        elapsed = toc - tic
        log.debug(f"Time: {elapsed:0.4f} seconds")
        self.assertLess(elapsed, 5, "took longer than 5 seconds")


if __name__ == "__main__":
    unittest.main()
