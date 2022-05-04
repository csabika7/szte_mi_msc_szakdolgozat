import os
import uuid


class ImageArchive:

    def __init__(self):
        self.location = os.environ["ARCHIVE_DIR"]

    def save(self, img: bytes):
        with open(os.path.join(self.location, "{}.png".format(uuid.uuid4())), mode="wb") as f:
            f.write(img)
