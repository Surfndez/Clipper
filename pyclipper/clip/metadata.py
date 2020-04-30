import os
from dataclasses import dataclass

from pyclipper.db import ClipperDb


@dataclass
class ClipMetadata:
    """Metadata about the video from which a clip was clipped."""

    title: str = None
    original_uploader: str = None
    original_video_url: str = None
    original_channel_url: str = None

    db = ClipperDb()

    def write_to_file_metadata(self, filepath):
        video_id = os.path.basename(filepath)
        self.db.save_video_info(
            video_id, self.title, self.original_video_url, self.original_channel_url
        )

    def read_from_file_metadata(self, filepath):
        video_id = os.path.basename(filepath)
        (
            _,
            self.title,
            self.original_video_url,
            self.original_channel_url,
        ) = self.db.get_video_info(video_id)
