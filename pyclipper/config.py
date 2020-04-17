import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("pyclipper/pyclipper.ini")

        twilio = self.config["twilio"]
        server = self.config["server"]
        files = self.config["files"]

        self._base_url = server["base_url"]
        self._flask_port = server.getint("flask_port")
        self._video_clip_complete_path = server["video_clip_complete_path"]
        self._account_sid = twilio["account_sid"]
        self._auth_token = twilio["auth_token"]
        self._phone_number = twilio["phone_number"]
        self._my_phone_number = twilio["my_phone_number"]
        self._demo_text = twilio["demo_text"]
        self._screenshot_mount_point = files["SCREENSHOT_MOUNT_POINT"]

    @property
    def base_url(self):
        return self._base_url

    @property
    def flask_port(self):
        return self._flask_port

    @property
    def video_clip_complete_path(self):
        return self._video_clip_complete_path

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
