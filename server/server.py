from urllib.parse import unquote

import pika
from flask import Flask, session
from flask import request
from flask import send_file
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# from pyclipper.request_parser import ClipperTextMessageParser
# from pyclipper.screenshot_metadata_parser import ScreenshotMetadataParser
from pyclipper.config import Config
from pyclipper.request import ClipperServerRequestData

c = Config()

SECRET_KEY = "a secret key"
app = Flask(__name__, static_folder="assets")
app.config.from_object(__name__)

client = Client(c.account_sid, c.auth_token)


@app.route("/")
def index():
    return f"""
        <p>Clipper</p>
        <p>Send Us a text with :</p>

        <ol>
            <li>A YouTube URL</li>
            <li>A start time</li>
            <li>An end time</li>
        </ol>
        <p>We'll send you a text with a download link to that clip</p>
        <a href="sms:+12029527509&body={c.demo_text}">Click here to text us!</a>
    """


@app.route("/clips/<clip>")
def clip_download(clip):
    # TODO: open graph protocol https://ogp.me/
    return send_file(f"assets/clips/{unquote(clip)}", as_attachment=True)


@app.route("/sms", methods=["GET", "POST"])
def on_text_received():
    """Callback triggered upon receiving a text from a user of Clipper™."""

    text = request.values.get("Body", None)
    from_number = request.values.get("From", None)
    image_url = None

    if request.values["NumMedia"] != "0":
        image_url = request.values["MediaUrl0"]

    r = ClipperServerRequestData(phone=from_number, image_url=image_url, text=text)

    queue_message(r)

    resp = MessagingResponse()
    resp.message(
        "We've received your request and will text you your clip URL when it's ready!"
    )
    # # session[from_number] = {"processing": True}
    return str(resp)


def queue_message(r: ClipperServerRequestData):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=r.json,
        properties=pika.BasicProperties(delivery_mode=2,),  # make message persistent
    )
    print(" [x] Sent %r" % r)
    connection.close()


@app.route(f"/{c.video_clip_complete_path}", methods=["POST"])
def clip_ready_webhook():

    clip_ready_response = request.get_json()

    secret = clip_ready_response.get("secret")
    if secret != c.secret:
        return "you dont belong here. I belong here. I inspired the Hopsins... goat 🐐"
    clip_url = clip_ready_response.get("clip_url")
    phone = clip_ready_response.get("phone")

    send_text(
        f"""
    Your clip is ready 📼 = ✅

    {clip_url}
    """,
        phone,
    )
    session[phone] = {"processing": False}
    return "needs protection"


def send_text(body, to):
    message = client.messages.create(body=body, from_=c.twilio_phone_number, to=to,)
    print(message.sid)


def start_server():
    app.run(port=c.flask_port)


if __name__ == "__main__":
    app.run(port=c.flask_port)
