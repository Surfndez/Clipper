import os
from unittest import TestCase

from xattr import xattr

from pyclipper.clip.metadata import ClipMetadata

filename = "tmp.txt"
key = "title"
value = "value"


# nodemon -e py --exec "python -m unittest test.test_read_write_metadata.TestMetadata"
class TestMetadata(TestCase):
    def test_create_metadata_from_file(self):
        # create file
        with open(filename, "w") as f:
            f.write(
                "test file will be deleted before you can even read this (unless you're debugging)"
            )

        attributes = xattr(filename)
        attributes.set(key, value.encode("utf-8"))

        m = ClipMetadata.read_from_file_metadata(filename)

        self.assertEqual(m.title, value)

    def test_write_metadata_to_file(self):
        m = ClipMetadata(title=value)
        m.write_to_file_metadata(filename)

        attributes = xattr(filename)
        attributes.get(key)

        self.assertEqual(m.title, value)

    @classmethod
    def tearDownClass(cls):
        os.remove(filename)
