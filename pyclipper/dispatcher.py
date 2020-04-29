import pika

from pyclipper.request import ClipperRequest
from pyclipper.request.request_type import RequestType
from pyclipper.request.response.response import ClipperResponse
from pyclipper.texting.texting import send_text


def format_response(clip_url):
    return (
        f"""
           Your clip is ready 📼 = ✅

           {clip_url}
           """,
    )


def dispatch_request(reqeust: ClipperRequest):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbit"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=reqeust.json,
        properties=pika.BasicProperties(
            # delivery_mode=2,
        ),  # make message persistent
    )

    print(" [x] Sent %r" % reqeust)
    connection.close()


def dispatch_phone_response(r: ClipperResponse):
    phone = r.request.response_destination

    send_text(
        format_response(clip_url=r.clip_url), phone,
    )


async def send_message(message, channel):
    await channel.send(message)


async def dispatch_discord_response(r: ClipperResponse):
    mention, channel = r.request.response_destination
    if r.error:
        await send_message(r.error, channel)
    else:
        await send_message(format_response(r.clip_url), channel)


async def dispatch_response(r: ClipperResponse):
    t = r.request.request_type
    if t == RequestType.phone:
        dispatch_phone_response(r)

    elif t == RequestType.discord:
        await dispatch_discord_response(r)
