import json
import re
from urllib.parse import unquote

import pika
from flask import Flask, session
from flask import request
from flask import send_file
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from pyclipper.config import Config
from pyclipper.request_parser import ClipperTextMessageParser, RequestArgumentException

c = Config()


SECRET_KEY = 'a secret key'
app = Flask(__name__, static_folder="assets")
app.config.from_object(__name__)

client = Client(c.account_sid, c.auth_token)


@app.route("/s")
def stest():
    session.clear()
    return "cleared"

@app.route("/")
def index():
    queue_message({
        "video_identifier": "https://www.youtube.com/watch?v=LYB00pdOnEc", "start": "4:44", "end": "5:14", "phone": "+16189808247"
    })
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
    return send_file(f"pyclipper/assets/clips/{unquote(clip)}", as_attachment=True)


def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


@app.route("/sms", methods=["GET", "POST"])
def on_text_received():
    """Callback triggered upon receiving a text from a user of Clipper™."""

    text_message = request.values.get("Body", None)
    from_number = request.values.get("From", None)

    number_session = session[from_number]
    # if number_session.get('processing', False):
    #     resp = MessagingResponse()
    #     resp.message("""
    #     It looks like you already have a video processing.
    #
    #     Only one at a time supported now.
    #
    #     Multiple clips at the same time coming soon.
    #     """)
    #     return str(resp)
    # number_session = session.get(from_number, {})
    # if is_url(text_message):
    #     number_session['url'] = text_message
    # elif text_message.count(':') >= 2 and text_message.count(' ') >= 1:
    #     number_session['times'] = text_message
    #
    # keys = number_session.keys()
    # do_process_request = 'url' in keys and 'times' in keys
    # number_session['processing'] = do_process_request
    # session[from_number] = number_session
    #
    # print(session[from_number])
    #
    # if not do_process_request:
    #     return ""

    try:
        parsed = ClipperTextMessageParser(text_message)
        msg = parsed.data
        msg['phone'] = from_number
    except RequestArgumentException:
        resp = MessagingResponse()
        resp.message(
            f"""
            We can't figure out that response. Please send a text with just the video URL, a start time and an end time.

            Here's an example:

            {c.demo_text}
            """
        )
        return str(resp)

    queue_message(msg)

    resp = MessagingResponse()
    resp.message(
        "We've received your request and will text you your clip URL when it's ready!"
    )
    session[from_number] = {"processing": True}
    return str(resp)


def queue_message(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2,),  # make message persistent
    )
    print(" [x] Sent %r" % msg)
    connection.close()


@app.route(f"/{c.video_clip_complete_path}", methods=["POST"])
def on_clip_ready():
    clip_ready_response = request.get_json()
    print(clip_ready_response)
    # TODO: Make Class for Ready Response
    clip_url = clip_ready_response.get('clip_url')
    phone = clip_ready_response.get('phone')
    send_text(f"""
    Your clip is ready (📼 = ✅)

    {clip_url}
    """, phone)
    session[phone] = {"processing": False}
    return "needs protection"


def send_text(body, to):
    message = client.messages.create(
        body=body,
        from_=c.twilio_phone_number,
        to=to,
    )
    print(message.sid)


def start_server():
    app.run(port=c.flask_port)


if __name__ == "__main__":
    app.run(port=c.flask_port)
