import re
from .base_handler import BaseHandler


class MegadriveHandler(BaseHandler):
    def test(self):
        if re.search(b'sega mega drive|sega genesis', self.file[0x100:0x110], re.I):
            print('Type: Megadrive ROM')
            return True

        return False
