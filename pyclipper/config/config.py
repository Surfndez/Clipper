import os
import configparser


config = configparser.ConfigParser()
config.read("pyclipper/pyclipper.ini")

twilio = config["twilio"]
discord = config["discord"]
server = config["server"]
files = config["files"]
clips = config["clips"]
ngrok = config["ngrok"]

base_url = server["base_url"]


def set_base_url(url):
    global base_url
    base_url = url


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

default_clip_length = clips["DEFAULT_CLIP_LENGTH"]

ngrok_auth = ngrok["ngrok_auth"]
ngrok_subdomain = ngrok["ngrok_subdomain"]
