from .megadrive import MegadriveHandler
from .iso9660 import ISO9660Handler
from .dreamcast import DCDataTrackHandler, GDIHandler

handlers = [MegadriveHandler, DCDataTrackHandler, ISO9660Handler, GDIHandler]
