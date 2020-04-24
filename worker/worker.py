from dataclasses import astuple

import pika

from pyclipper.config import Config
from pyclipper.dispatcher import dispatch_response
from pyclipper.request import ClipperRequest
from pyclipper.request.parser.parser import parse_incoming_clipper_text_request
from pyclipper.request.response.response import ClipperResponse
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
    request = ClipperRequest(request_json=body.decode("utf-8"))
    try:
        url, start_seconds, end_seconds, _ = astuple(
            parse_incoming_clipper_text_request(request)
        )

        clip_url = download_and_trim(url, start_seconds, end_seconds)

        response = ClipperResponse(request, clip_url)
        dispatch_response(response)
    except:
        error_message = "Something wen't wrong. I'll try and fix it but no promises since this is a Hackathon project :)"
        response = ClipperResponse(request, error=error_message)
        dispatch_response(response)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


channel.basic_qos(prefetch_count=0)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

channel.start_consuming()
