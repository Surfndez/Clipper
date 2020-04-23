from dataclasses import dataclass, asdict
from pathlib import Path

from xattr import xattr


@dataclass
class ClipMetadata:
    """Metadata about the video from which a clip was clipped."""

    title: str = None
    original_uploader: str = None
    original_video_url: str = None
    original_channel_url: str = None

    def write_to_file_metadata(self, filepath):
        filepath = Path(filepath).resolve()
        metadata = xattr(filepath)
        for k, v in asdict(self).items():
            if v:
                b = v if isinstance(v, bytes) else v.encode("utf-8")
                metadata.set(k, b)

    @staticmethod
    def read_from_file_metadata(filepath):
        filepath = Path(filepath).resolve()
        attributes = xattr(filepath)
        metadata = ClipMetadata()

        for k in asdict(metadata).keys():
            try:
                setattr(metadata, k, attributes.get(k).decode())
            except IOError:
                pass

        return metadata
