import os
from urllib.parse import quote

import ffmpeg
import youtube_dl
from requests.compat import urljoin

from pyclipper.clip.metadata import ClipMetadata
from pyclipper.config import Config

c = Config()


def youtube_channel_template(id):
    return f"https://www.youtube.com/channel/{id}"


def download_and_trim(video_url, start, end=None):
    if end is None:
        end = start + c.default_clip_length

    if end < start:
        start, end = end, start

    if not isinstance(video_url, str):
        return

    # TODO move to config
    videos = "server/assets"
    full_video_path = f"{videos}/full"
    clips_path = f"{videos}/clips"

    if not os.path.exists(full_video_path):
        os.mkdir(full_video_path)
    if not os.path.exists(clips_path):
        os.mkdir(clips_path)

    extension = ".mp4"

    template = "server/assets/full/%(id)s.%(ext)s"

    ydl_opts = {"outtmpl": template, "format": "mp4"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info["title"]

        # YouTube relevant
        uploader = info.get("uploader")
        channel_id = info.get("channel_id")

        creator = info.get("creator")
        channel = info.get("channel")

        # YouTube relevant
        print("title:\t\t", title)
        print("uploader:\t\t", uploader)
        print("video_url:\t\t", video_url)
        print("channel url:\t\t", youtube_channel_template(channel_id))

        # YouTube None
        print("creator:\t\t", creator)
        print("channel:\t\t", channel)

        video_id = info["id"]
        ext = info["ext"]

        video = f"{full_video_path}/{video_id}.{ext}"
        clip_name = f"{video_id}-s{start}-e{end}{extension}"
        clip_path = os.path.join(clips_path, clip_name)

        if not os.path.exists(video):
            ydl.download([video_url])

    if not os.path.exists(clip_path):
        "ffmpeg " "-i iXwfBJYCTc4.mp4 " "-ss 4 " "-to 2:44 " "-c:v copy " "-c:a copy" " clip.mp4"
        ffmpeg.input(video, ss=start, to=end).output(
            clip_path,
            vcodec="copy",
            acodec="copy"
            # , hide_banner=True, loglevel="panic"
        ).run()

        metadata = ClipMetadata(
            title, uploader, video_url, youtube_channel_template(channel_id)
        )

        metadata.write_to_file_metadata(clip_path)

    return urljoin(c.base_url, f"clips/{clip_name}")
