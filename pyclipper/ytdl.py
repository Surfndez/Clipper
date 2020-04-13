import os
from urllib.parse import quote

import ffmpeg
import youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from requests.compat import urljoin

from pyclipper.config import Config

c = Config()


class EndTimeNeededError(Exception):
    def __init__(self):
        self.message = "End Time Required."
        super(EndTimeNeededError, self).__init__(self.message)


def download_and_trim(video_identifier, start, end=None):
    if end is None:
        raise EndTimeNeededError()

    if not isinstance(video_identifier, str):
        return

    videos = "pyclipper/assets"
    full_video_path = f"{videos}/full"
    clips_path = f"{videos}/clips"
    extension = ".mp4"

    template = "pyclipper/assets/full/%(id)s.%(ext)s"

    ydl_opts = {"outtmpl": template, "format": "mp4"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_identifier, download=False)
        title = info["title"]
        video_id = info["id"]
        ext = info["ext"]

        video = f"{full_video_path}/{video_id}.{ext}"
        clip_name = f"{title}-s{start}-e{end}{extension}"
        target = os.path.join(clips_path, "buggy" + clip_name)
        clip_path = os.path.join(clips_path, clip_name)

        if not os.path.exists(video):
            ydl.download([video_identifier])

    # ffmpeg_extract_subclip has a bug on some videos
    # When I attempt to extract a three second clip from this video
    # https://twitter.com/i/status/1246637822959693825
    # the clip is extracted and shows the first three seconds but then the video
    # freezes and runs until 5 seconds. The second call to ffmpeg.input... fixes this
    # Solution would be to use ffmpeg.input to extract the clip in the first place,
    # but I've got to read more about the library
    if not os.path.exists(clip_path):
        ffmpeg_extract_subclip(video, start, end, targetname=target)
        ffmpeg.input(target).output(clip_path).run()
        os.remove(target)

    return urljoin(c.base_url, f"clips/{quote(clip_name)}")
