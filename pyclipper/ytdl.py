import logging
import os

import ffmpeg
import youtube_dl
from requests.compat import urljoin

from pyclipper.config.config import (
    base_url,
    default_clip_length,
    full_video_mount_point,
    clips_mount_point,
    video_name_template,
)
from pyclipper.db import ClipperDb
from pyclipper.utils import build_clip_file_path

db = ClipperDb()

log = logging.getLogger(__name__)


def youtube_channel_template(id):
    return f"https://www.youtube.com/channel/{id}"


def download_and_trim(video_url, start, end=None):
    if end is None:
        end = start + default_clip_length

    if end < start:
        start, end = end, start

    if not isinstance(video_url, str):
        return

    full_video_path = full_video_mount_point
    clips_path = clips_mount_point

    log.info("Full video path: " + full_video_path)
    log.info("Clips path: " + clips_path)

    if not os.path.exists(full_video_path):
        os.makedirs(full_video_path)
    if not os.path.exists(clips_path):
        os.makedirs(clips_path)

    ydl_opts = {"outtmpl": video_name_template, "format": "mp4"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

        # YouTube relevant
        title = info["title"]
        uploader = info.get("uploader")
        channel_id = info.get("channel_id")

        creator = info.get("creator")
        channel = info.get("channel")

        # YouTube relevant
        log.debug(f"title:\t\t{title}")
        log.debug(f"uploader:\t\t{uploader}")
        log.debug(f"video_url:\t\t{video_url}")
        log.debug(f"channel url:\t\t{youtube_channel_template(channel_id)}")

        # YouTube not relevant
        log.debug(f"creator:\t\t{creator}")
        log.debug(f"channel:\t\t{channel}")

        video_id = info["id"]
        ext = info["ext"]

        video = f"{full_video_path}/{video_id}.{ext}"
        url_clip_name_params = f"video_id={video_id}&start={start}&end={end}"
        clip_path = build_clip_file_path(video_id, start, end)

        if not os.path.exists(video):
            ydl.download([video_url])

    if not os.path.exists(clip_path):
        "ffmpeg " "-i iXwfBJYCTc4.mp4 " "-ss 4 " "-to 2:44 " "-c:v copy " "-c:a copy" " clip.mp4"
        stream = ffmpeg.input(video, ss=start, to=end).output(
            clip_path,
            vcodec="copy",
            acodec="copy"
            # , hide_banner=True, loglevel="panic"
        )

        log.info(ffmpeg.get_args(stream))

        stream.run()

        db.save_video_info(
            video_id, title, video_url, youtube_channel_template(channel_id)
        )

    return urljoin(base_url, f"clips?{url_clip_name_params}")
