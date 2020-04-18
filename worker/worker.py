import json
import pika
import requests
from pyclipper.config import Config
from pyclipper.parser import parse_clipper_request_contents
from pyclipper.request import ClipperServerRequestData
from pyclipper.ytdl import download_and_trim

c = Config()

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    r = ClipperServerRequestData(request_json=body)
    # at this point, r contains and image url, text, and a phone number
    # next step is to parse it
    url, start_seconds, end_seconds = parse_clipper_request_contents(r)

    clip_url = download_and_trim(url, start_seconds, end_seconds,)

    requests.post(
        f"http://localhost:{c.flask_port}/{c.video_clip_complete_path}",
        json={"clip_url": clip_url, **d},
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
