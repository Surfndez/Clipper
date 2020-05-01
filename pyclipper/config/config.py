import os
import configparser
import logging

log = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read("pyclipper/pyclipper.ini")

twilio = config["twilio"]
discord = config["discord"]
server = config["server"]
files = config["files"]
clips = config["clips"]
ngrok = config["ngrok"]

flask_port = server.getint("flask_port")

twilio_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
twilio_auth_token = os.environ["TWILIO_AUTH_TOKEN"]

twilio_phone_number = twilio["phone_number"]
my_phone_number = twilio["my_phone_number"]
demo_text = twilio["demo_text"]

bot_token = discord["bot_token"]

screenshot_mount_point = files["SCREENSHOT_MOUNT_POINT"]
full_video_mount_point = files["FULL_VIDEOS_MOUNT_POINT"]
clips_mount_point = files["CLIPS_VIDEOS_MOUNT_POINT"]
video_name_template = files["FULL_VIDEO_NAME_TEMPLATE"]

default_clip_length = int(clips["DEFAULT_CLIP_LENGTH"])

ngrok_auth = ngrok["ngrok_auth"]
ngrok_subdomain = ngrok["ngrok_subdomain"]


def log_config():
    log.info(
        "\n".join(
            f"{k: <25} - {v}" for k, v in globals().items() if not k.startswith("__")
        )
    )


public_url_cache_file = ".public_url_cache_file.txt"


def cache_public_url(url):
    with open(public_url_cache_file, "w") as url_fd:
        url_fd.write(url)


def read_public_url():
    return open(public_url_cache_file, "r").read()
