from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {"hdf5"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ModelFileHandler:

    def __init__(self, file_input: FileStorage, storage_path: str):
        self.file_input = file_input
        self.storage_path = storage_path

    def save(self):
        if allowed_file(self.file_input.filename):
            file_name = secure_filename(self.file_input.filename)
            self.file_input.save(os.path.join(self.storage_path, file_name))
            return file_name
        else:
            raise InvalidFileExtension("Invalid file extension. File name: {}", self.file_input.filename)


class InvalidFileExtension(Exception):
    pass
