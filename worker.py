import json
import pika
import requests
from pyclipper.config import Config
from pyclipper.ytdl import download_and_trim

c = Config()

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="task_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    d = json.loads(body)

    clip_url = download_and_trim(
        d.get("url"), d.get("start_seconds"), d.get("end_seconds"),
    )

    requests.post(
        f"http://localhost:{c.flask_port}/{c.video_clip_complete_path}",
        json={"clip_url": clip_url, **d},
    )
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
