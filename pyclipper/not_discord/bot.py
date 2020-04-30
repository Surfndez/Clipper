import os
import logging

from discord.ext import commands
from pika.exceptions import AMQPConnectionError

from pyclipper.dispatcher import dispatch_request, dispatch_response
from pyclipper.request import ClipperRequest
from pyclipper.request.request_type import RequestType
from pyclipper.request.response.response import ClipperResponse

log = logging.getLogger(__name__)

description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""
bot = commands.Bot(command_prefix="?", description=description)


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user.name} (id: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    mention = message.author.mention

    image_ext = [".jpg", ".png", ".jpeg"]
    images = [
        attachment
        for attachment in message.attachments
        if os.path.splitext(attachment)[1] in image_ext
    ]

    image_url = None if not len(images) else images[0]
    text = message.content

    r = ClipperRequest(
        RequestType.discord, (mention, message.channel), image_url=image_url, text=text
    )

    try:
        dispatch_request(r)

        response = (
            f"I received your request {mention}. Give me a sec to pwn the n00bs... "
        )
        await message.channel.send(response)
    except AMQPConnectionError:
        await dispatch_response(
            ClipperResponse(
                r,
                error="Looks like the message queue isn't ready. Please send an aggressive Tweet to https://twitter.com/technoplato to get me to fix this.",
            )
        )


bot.run()
