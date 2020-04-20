from dataclasses import dataclass
import json


@dataclass
class ClipperServerRequestData:
    def __init__(self, phone=None, image_url=None, text=None, request_json=None):
        if request_json is not None:
            self.__dict__ = json.loads(request_json)
        else:
            self.phone = phone
            self.image_url = image_url
            self.text = text

    @property
    def json(self):
        return json.dumps(vars(self))

    def __repr__(self):
        return f"""phone\t{self.phone}    
                   image\t{self.image_url}    
                   text\t{self.text}"""
