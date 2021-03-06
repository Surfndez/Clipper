import os
import logging
import urllib

from flask import Flask
from flask import request
from flask import send_file
from flask import send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

from pyclipper.config.config import (
    default_clip_length,
    demo_text,
    twilio_phone_number,
    flask_port,
)
from pyclipper.db import ClipperDb
from pyclipper.dispatcher import dispatch_request
from pyclipper.request import ClipperRequest
from pyclipper.request.request_type import RequestType
from pyclipper.utils import build_clip_file_path


SECRET_KEY = "a secret key"
app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)

log = logging.getLogger(__name__)
db = ClipperDb()


# TODO: templates
@app.route("/")
def index():
    return f"""
        <!DOCTYPE html>

        <head>
            <style>
                body {{
                    font-size: 48px;
                    padding: 16px;
                }}
            </style>
        </head>

        <body>
            <p>Clipper</p>
            <a href="sms:{twilio_phone_number}&body={demo_text}">Click here to text us!</a>
            <p>Send a text to {twilio_phone_number} with:</p>
            <ol>
                <li>A Video URL</li>
                <li>A start time</li>
                <li>An end time</li>
            </ol>

            <p>You can also send us a screenshot of a YouTube video in vertical orientation.</p>

            <p>We'll send you a text with a download link to that clip</p>
            <a href="sms:{twilio_phone_number}&body={demo_text}">Click here to text us!</a>

            <div>
                <a href="https://dev.to/technoplato">Created by Michael Lustig</a> | 
                <a href="https://twitter.com/technoplato">twitter</a> | 
                <a href="https://github.com/technoplato">github</a> 
            </div>
        </body>

        </html>
    """


@app.route("/static/<path:filename>")
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, "static"), filename)


@app.route("/clips")
def clip_view():

    video_id = request.values.get("video_id", None)
    start = request.values.get("start", None)
    end = request.values.get("end", None)

    forward_params = f"video_id={video_id}&start={start}&end={end}"

    clip_path = build_clip_file_path(video_id, start, end)
    clip_file = os.path.basename(clip_path)

    return f"""
<!DOCTYPE html>
<head>
    <style>
        body {{
            font-size: 48px;
            padding: 16px;
        }}
    </style>
</head>
<body>
    <video controls width="100%">

    <source src="static/{clip_file}"
            type="video/webm">

    <source src="static/{clip_file}"
            type="video/mp4">

    Sorry, your browser doesn't support embedded videos.
    </video>
    <div>
    <a href="downloads?clip_path=static/{clip_file}&{forward_params}">Download</a>
    </div>
</body>
</html>
"""


@app.route("/downloads")
def clip_download():

    clip_path = request.values.get("clip_path")
    video_id = request.values.get("video_id", None)
    start = request.values.get("start", None)
    end = request.values.get("end", None)

    video = db.get_video_info(video_id)

    clip_path = build_clip_file_path(video_id, start, end)
    clip_file = os.path.basename(clip_path)

    # TODO: open graph protocol https://ogp.me/
    return send_file(
        clip_path, as_attachment=True, attachment_filename=f"Clip of {video[1]}.mp4",
    )


@app.route("/sms", methods=["GET", "POST"])
def twilio_webhook():
    """Callback triggered upon receiving a text from a user of Clipper™."""

    text = request.values.get("Body", None)
    from_number = request.values.get("From", None)
    image_url = None

    if request.values["NumMedia"] != "0":
        image_url = request.values["MediaUrl0"]

    log.debug(
        f"Twilio webhook called"
        f"\n\t(text: {text})\n"
        f"\n\t(RequestType.phone: {RequestType.phone})\n"
        f"\n\t(from_number: {from_number})\n"
    )

    r = ClipperRequest(
        request_type=RequestType.phone,
        response_destination=from_number,
        image_url=image_url,
        text=text,
    )

    dispatch_request(r)

    return str(
        MessagingResponse().message(
            "We've received your request and will text you your clip URL when it's ready!"
        )
    )


def start_server():
    app.run(host="0.0.0.0", port=flask_port)


if __name__ == "__main__":
    start_server()
