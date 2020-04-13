import os
import unittest

from pyclipper.ytdl import download_and_trim

videos = "pyclipper/assets"
full_video_path_prefix = f"{videos}/full"
clips_path_prefix = f"{videos}/clips"

youtube_id = "iXwfBJYCTc4"
desired_full_video = f"{full_video_path_prefix}/{youtube_id}.mp4"
desired_clip_path = f"{clips_path_prefix}/Gordon Ramsay Cooks Buffalo For A Cambodian Tribe | Gordon's Great Escape-s4-e284.mp4"


class TestFilenames(unittest.TestCase):
    def test_files_named_appropriately(self):
        # pass
        download_and_trim("11-lpoJHu0U", 4, 284)
        self.assertTrue(os.path.exists(desired_full_video))
        self.assertTrue(os.path.exists(desired_clip_path))


if __name__ == "__main__":
    unittest.main()
