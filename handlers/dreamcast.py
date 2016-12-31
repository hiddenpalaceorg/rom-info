import mmap
import os.path
import re
from collections import OrderedDict
from .base_handler import BaseHandler
from .iso9660 import ISO9660Handler
from utils import MmappedFile, ConcatenatedFile


class GDIParseError(ValueError):
    pass


class GDIHandler(BaseHandler):
    def test(self):
        if not re.match('^.*\.gdi', self.file_name, re.IGNORECASE):
            return False

        try:
            self.parse()
        except GDIParseError:
            return False

        return True

    def parse(self):
        text = self.read(0, 8*1024)

        lines = text.decode('ascii').splitlines()
        if len(lines) == 1:
            raise GDIParseError

        try:
            n_tracks = int(lines.pop(0))
        except ValueError:
            raise GDIParseError

        if len(lines) != n_tracks:
            print(len(lines), n_tracks)
            raise GDIParseError

        # TODO figure out complete format
        tracks = []
        for track_i, line in enumerate(lines):
            try:
                match = re.match('(?P<index>\d+) (?P<sector>\d+) (?P<type>\d+) (?P<sector_size>\d+)'
                                 ' (?P<file_name>\S+) (\d+)', line)

                if not match:
                    raise GDIParseError

                track = match.groupdict()

                for key in ('index', 'sector', 'type', 'sector_size'):
                    track[key] = int(track[key])

                if track['index'] != track_i + 1:
                    raise GDIParseError

                tracks.append(track)

            except ValueError:
                raise GDIParseError

        return tracks

    def get_info(self):
        tracks = self.parse()
        for track in tracks:
            track['path'] = os.path.join(os.path.dirname(self.file_name), track['file_name'])

        if len(tracks) > 3 and tracks[2]['type'] == 4 and tracks[-1]['type'] == 4:
            # Dreamcast discs often contain two data tracks (track 3 and the last track) in addition to track 1.
            mixed_mode = True

        else:
            mixed_mode = False

        track_info = OrderedDict()
        for track in tracks:
            if mixed_mode and track == tracks[-1]:
                continue

            if mixed_mode and track['index'] == 3:
                last_track = tracks[-1]
                offset_gap = (last_track['sector'] - track['sector']) * 2352
                track_name = 'Track {}+{}'.format(track['index'], last_track['index'])

                file = ConcatenatedFile(file_names=[track['path'], last_track['path']],
                                        offsets=[0, offset_gap])  # TODO handle different sector sizes

            else:
                track_name = 'Track {}'.format(track['index'])
                file = MmappedFile(track['path'])

            with file:
                if track['type'] == 4:
                    handler = DCDataTrackHandler(file=file, file_name=track['file_name'], sector_offset=track['sector'], track_name=track_name)
                    if handler.test():
                        handler.get_info()
                        track_info[track_name] = handler.info
                    else:
                        track_info[track_name] = 'Data track in unknown format'

                elif track['type'] == 0:
                    track_info[track_name] = 'Audio track'

                else:
                    track_info[track_name] = 'Unknown'

        self.info['Tracks'] = track_info


class DCDataTrackHandler(ISO9660Handler):
    def test(self):
        if not super().test():
            return False

        if self.read(0, 16) == b'SEGA SEGAKATANA ':
            return True
        else:
            return False

    def get_info(self):
        header_info = OrderedDict()
        header_info['Hardware ID'] = self.unpack('string', 0x00, 16, 0)
        header_info['Maker ID'] = self.unpack('string', 0x10, 16, 0)
        header_info['CRC'] = self.unpack('string', 0x20, 4, 0)
        header_info['Device'] = self.unpack('string', 0x25, 6, 0)
        header_info['Disc'] = self.unpack('string', 0x2b, 3, 0)
        header_info['Region'] = self.unpack('string', 0x30, 8, 0).strip()
        header_info['Peripherals'] = self.unpack('string', 0x38, 8, 0)
        header_info['Product number'] = self.unpack('string', 0x40, 10, 0)
        header_info['Product version'] = self.unpack('string', 0x4a, 6, 0)
        header_info['Release date'] = self.unpack('string', 0x50, 16, 0)
        header_info['Boot file'] = self.unpack('string', 0x60, 16, 0)
        header_info['Company name'] = self.unpack('string', 0x70, 16, 0)
        header_info['Software name'] = self.unpack('string', 0x80, 16, 0)

        self.info['Header'] = header_info

        super().get_info()
