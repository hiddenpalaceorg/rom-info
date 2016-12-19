from collections import OrderedDict


class BaseHandler:
    def __init__(self, file, file_name):
        self.file = file
        self.file_name = file_name
        self.info = OrderedDict()

    def read(self, offset, size):
        return self.file[offset:offset + size]
