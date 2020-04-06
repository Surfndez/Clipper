import logging
import os
from urllib.parse import quote
import ffmpeg
import youtube_dl
from durations import Duration
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from requests.compat import urljoin

logger = logging.getLogger(__name__)

ngrok = "https://4578c91c.ngrok.io"
# TODO: ENV config
base = ngrok

class EndTimeNeededError(Exception):
    def __init__(self):
        self.message = "End Time Required."
        super(EndTimeNeededError, self).__init__(self.message)


def download_and_trim(video_identifier, start, end=None):
    if end is None:
        raise EndTimeNeededError()

    start_seconds = Duration(start).to_seconds()
    end_seconds = Duration(end).to_seconds()

    videos = "pyclipper/assets"
    full = f"{videos}/full"
    clips = f"{videos}/clips"
    extension = ".mp4"

    template = "pyclipper/assets/full/%(title)s-%(id)s.%(ext)s"
    print(template)

    ydl_opts = {"outtmpl": template,
                # "format": "137"
                }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_identifier, False)
        title = info['title']
        video_id = info['id']
        ext = info['ext']
        video = f"{full}/{title}-{video_id}.{ext}"
        clip_name = f"{title}-{video_id}-s{start_seconds}-e{end_seconds}{extension}"
        target = os.path.join(clips, "buggy" + clip_name)
        clip_path = os.path.join(clips, clip_name)

        if not os.path.exists(video):
            ydl.download([video_identifier])

    # ffmpeg_extract_subclip has a bug on some videos
    # When I attempt to extract a three second clip from this video
    # https://twitter.com/i/status/1246637822959693825
    # the clip is extracted and shows the first three seconds but then the video
    # freezes and runs until 5 seconds. The second call to ffmpeg.input... fixes this
    # Solution would be to use ffmpeg.input to extract the clip in the first place,
    # but I've got to read more about the library
    ffmpeg_extract_subclip(video, start_seconds, end_seconds, targetname=target)
    ffmpeg.input(target).output(clip_path).run()
    os.remove(target)
    return urljoin(base, f"clips/{quote(clip_name)}")



