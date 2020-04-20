import os
from urllib.parse import quote

import ffmpeg
import youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from requests.compat import urljoin

from pyclipper.config import Config

c = Config()


def download_and_trim(video_identifier, start, end=None):
    if end is None:
        end = start + c.default_clip_length

    if end < start:
        start, end = end, start

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
        clip_path = os.path.join(clips_path, clip_name)

        if not os.path.exists(video):
            ydl.download([video_identifier])

    if not os.path.exists(clip_path):
        "ffmpeg " "-i iXwfBJYCTc4.mp4 " "-ss 4 " "-to 2:44 " "-c:v copy " "-c:a copy" " clip.mp4"
        ffmpeg.input(video, ss=start, to=end).output(
            clip_path, vcodec="copy", acodec="copy"
        ).run()

    return urljoin(c.base_url, f"clips/{quote(clip_name)}")
