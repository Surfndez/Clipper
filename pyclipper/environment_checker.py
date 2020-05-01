import os
import logging

from pyclipper.config.config import twilio_account_sid, twilio_auth_token

logger = logging.getLogger(__name__)
d = logger.debug


def check_google_cloud_vision_environment_variables():
    google_cloud_vision_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    google_credentials_missing = (
        google_cloud_vision_credentials is None
        or len(google_cloud_vision_credentials) == 0
    )
    if google_credentials_missing:
        d("Google Credentials Missing.")
        raise Exception(
            """
In order to use Clipper, please open the .env file in the root of the project and tell it where you downloaded your Google Cloud Platform key.json.

If you don't have a key for Google Cloud Vision, please go here, follow the instructions, and then tell the .env file where you downloaded the key: 

https://cloud.google.com/vision/docs/quickstart-client-libraries

"""
        )


def check_twilio_environment_variables():
    twilio_credentials_missing = twilio_account_sid is None or twilio_auth_token is None
    if twilio_credentials_missing:
        d("Twilio Credentials Missing.")
        raise Exception(
            """
In order to use Clipper, please open the .env file in the root of the project and copy in your Twilio SID and Auth Token.

If you don't have a Twilio account, please go here to create one.

https://www.twilio.com/try-twilio?promo=Gbv52f
"""
        )


def check_environment_variables():
    d(os.environ)
    check_google_cloud_vision_environment_variables()
    check_twilio_environment_variables()
