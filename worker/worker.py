from dataclasses import astuple

import pika
import requests

from pyclipper.config import Config
from pyclipper.request import ClipperServerRequestData
from pyclipper.request.parser.parser import parse_incoming_clipper_text_request
from pyclipper.ytdl import download_and_trim

c = Config()

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    # print(body)
    # ch.basic_ack(delivery_tag=method.delivery_tag)
    # pass
    r = ClipperServerRequestData(request_json=body.decode("utf-8"))
    url, start_seconds, end_seconds, _ = astuple(parse_incoming_clipper_text_request(r))

    clip_url = download_and_trim(url, start_seconds, end_seconds)

    requests.post(
        f"http://localhost:{c.flask_port}/{c.video_clip_complete_path}",
        json={"clip_url": clip_url, "phone": r.phone, "secret": c.secret},
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


channel.basic_qos(prefetch_count=0)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
