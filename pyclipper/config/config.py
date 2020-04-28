import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("pyclipper/pyclipper.ini")

        twilio = self.config["twilio"]
        discord = self.config["discord"]
        server = self.config["server"]
        files = self.config["files"]
        clips = self.config["clips"]

        self._base_url = server["base_url"]
        self._flask_port = server.getint("flask_port")
        self._secret = server["secret"]

        self._account_sid = twilio["account_sid"]
        self._auth_token = twilio["auth_token"]
        self._phone_number = twilio["phone_number"]
        self._my_phone_number = twilio["my_phone_number"]
        self._demo_text = twilio["demo_text"]

        self._bot_token = discord["bot_token"]

        self._screenshot_mount_point = files["SCREENSHOT_MOUNT_POINT"]
        self._full_video_mount_point = files["FULL_VIDEOS_MOUNT_POINT"]
        self._clips_mount_point = files["CLIPS_VIDEOS_MOUNT_POINT"]
        self._video_name_template = files["FULL_VIDEO_NAME_TEMPLATE"]

        self._DEFAULT_CLIP_LENGTH = clips["DEFAULT_CLIP_LENGTH"]

    @property
    def base_url(self):
        return self._base_url

    @property
    def flask_port(self):
        return self._flask_port

    @property
    def account_sid(self):
        return self._account_sid

    @property
    def auth_token(self):
        return self._auth_token

    @property
    def twilio_phone_number(self):
        return self._phone_number

    @property
    def my_phone_number(self):
        return self._my_phone_number

    @property
    def demo_text(self):
        return self._demo_text

    @property
    def screenshot_mount_point(self):
        return self._screenshot_mount_point

    @property
    def full_video_mount_point(self):
        return self._full_video_mount_point

    @property
    def clips_mount_point(self):
        return self._clips_mount_point

    @property
    def video_name_template(self):
        return self._video_name_template

    @property
    def default_clip_length(self):
        return int(self._DEFAULT_CLIP_LENGTH)
