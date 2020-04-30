from twilio.rest import Client

from pyclipper.config import Config

c = Config()
client = Client(c.account_sid, c.auth_token)


def send_text(body, to):
    message = client.messages.create(
        body=body, from_=c.twilio_phone_number, to=to,)


def lookup(number):
    return client.lookups.phone_numbers(number).fetch(type=["carrier"])
