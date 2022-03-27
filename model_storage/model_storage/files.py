from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {"hdf5"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ModelFileHandler:

    def __init__(self, file: FileStorage, storage_path):
        self.file = file
        self.storage_path = storage_path

    def save(self):
        if allowed_file(self.file.filename):
            file_name = secure_filename(self.file.filename)
            self.file.save(os.path.join(self.storage_path, file_name))
            return file_name
        else:
            raise InvalidFileExtension("Invalid file extension. File name: {}", self.file.filename)


class InvalidFileExtension(Exception):
    pass
