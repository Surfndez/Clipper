from twilio.rest import Client

from pyclipper.config.config import twilio_account_sid, twilio_auth_token

client = Client(twilio_account_sid, twilio_auth_token)


def send_text(body, to):
    client.messages.create(
        body=body, from_=c.twilio_phone_number, to=to,
    )


def lookup(number):
    return client.lookups.phone_numbers(number).fetch(type=["carrier"])
