import json
import os
from urllib.parse import unquote

import pika
from flask import Flask
from flask import request
from flask import send_file
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# from pyclipper.request_parser import RequestParser
from pyclipper.config import Config
from pyclipper.request_parser import ClipperTextMessageParser, RequestArgumentException

app = Flask(__name__, static_folder="assets")

c = Config()

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
    return send_file(f"assets/clips/{unquote(clip)}", as_attachment=True)


@app.route("/sms", methods=["GET", "POST"])
def on_text_received():
    """Callback triggered upon receiving a text from a user of Clipper™."""
    body = request.values.get("Body", None)
    from_number = request.values.get("From", None)

    print(from_number, body)

    try:
        p = ClipperTextMessageParser(body)
        print(p)
    except RequestArgumentException:
        resp = MessagingResponse()
        resp.message(
            f"We can't figure out that response. Please send a text with just the video URL, a start time and an end "
            f"time. \n\nHere's an example:\n\n{c.demo_text} "
        )
        return str(resp)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(p.data),
        properties=pika.BasicProperties(delivery_mode=2,),  # make message persistent
    )
    print(" [x] Sent %r" % p.data)
    connection.close()

    resp = MessagingResponse()
    resp.message(
        "We've received your request and will text you your clip URL when it's ready!"
    )

    return str(resp)


@app.route(f"/{c.video_clip_complete_path}", methods=["POST"])
def on_clip_ready():
    # body = request.get_json()
    # finished_clip_url = body['youtube']
    # import q
    # q.d()
    # print(request.HTTP_HOST)
    return "needs protection"


def send_text(body, to):
    message = client.messages.create(
        body=body,
        from_=c.twilio_phone_number,
        to=to,
    )
    print(message.sid)


if __name__ == "__main__":
    app.run(port=c.flask_port)
