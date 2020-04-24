from dataclasses import dataclass
import json

# TODO add request methodologies and request Ids and then base dispatching off of that request type
# ✅ phone - phone number
# ✅ discord - discord channel / user id to respond to
# slack - discord channel / user id to respond to
# api - push notification ID
# we just need to be able to asyncrhonously responc
# , etc
from typing import Any

from pyclipper.request.request_type import RequestType


@dataclass
class ClipperRequest:
    def __init__(
        self,
        request_type: RequestType,
        response_destination: Any,
        image_url: str = None,
        text: str = None,
        request_json=None,
    ):
        if request_json is not None:
            self.__dict__ = json.loads(request_json)
        elif not request_type or not response_destination:
            raise Exception("I need these to respond to the request")
        else:
            self.request_type = request_type
            self.response_destination = response_destination
            self.image_url = image_url
            self.text = text

    @property
    def json(self):
        return json.dumps(vars(self))
