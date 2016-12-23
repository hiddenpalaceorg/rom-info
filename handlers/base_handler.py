from collections import OrderedDict


class BaseHandler:
    def __init__(self, file, file_name):
        self.file = file
        self.file_name = file_name
        self.info = OrderedDict()

    def read(self, offset, size):
        if offset < 0:
            raise IndexError("File offset must be greater than 0")

        if offset + size >= len(self.file):
            raise IndexError("Cannot read beyond the end of the file")

        return self.file[offset:offset + size]
