"""
Handle ISO 9660 disc image files.

Format reference: http://wiki.osdev.org/ISO_9660
"""
import os
import re
import struct
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from zlib import crc32
import config
from utils import print_status
from .base_handler import BaseHandler


class ISO9660Handler(BaseHandler):
    def __init__(self, sector_offset=0, track_name="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sector_offset = sector_offset
        self.track_name = track_name

        self.format = None
        self.sector_size = None
        self.pvd_sector = None

        self._edc_table = None

        self.skip_offset = None
        self.data_offset = None

    def test(self):
        # TODO: do this per-sector (for multi-track files)
        if self.read_raw(0x9311, 5) == b'CD001' and self.read_raw(0x0f, 1) == b'\x01':
            self.format = 'mode1'
            self.sector_size = 2352
            self.skip_offset = 0
            self.data_offset = 0x10
            return True

        elif self.read_raw(0x9319, 5) == b'CD001' and self.read_raw(0x0f, 1) == b'\x02':
            self.format = 'mode2'
            self.sector_size = 2352
            self.skip_offset = 0x10
            self.data_offset = 0x18
            return True

        elif self.read_raw(0x8001, 5) == b'CD001':
            self.format = 'iso'
            self.sector_size = 2048
            self.skip_offset = 0
            self.data_offset = 0

            return True

        else:
            return False

    def data_size(self, sector):
        if self.format == 'mode1':
            return 2048

        elif self.format == 'mode2':
            if self.sector_form(sector) == 1:
                return 2048

            elif self.sector_form(sector) == 2:
                return 2324

            else:
                raise ValueError("Unknown Mode 2 form")

        elif self.format == 'iso':
            return 2048

        raise ValueError("Unknown disc format")

    def sector_form(self, sector):
        if (self.read(0x12, 1, sector, raw=True)[0] & 0x20) == 0:
            return 1

        else:
            return 2

    def edc_offset(self, sector):
        if self.format not in ('mode1', 'mode2'):
            return None

        return self.data_offset + self.data_size(sector)  # EDC always follows user data

    def ecc_offset(self, sector):
        if self.format == 'mode1' or (self.format == 'mode2' and self.sector_form(sector) == 1):
            return 0x81c

        return None

    def get_info(self):
        """Get volume information from the primary volume descriptor of the ISO 9660 image."""

        # Find primary volume descriptor (vd_type == 1).
        pvd_sector = None
        for sector in range(0x10, 0x80):
            if self.read(1, 5, sector) != b'CD001':
                # Not a volume descriptor, give up.
                break

            vd_type = self.unpack('uint8', 0, 1, sector=sector)

            if vd_type == 1:
                # Primary volume descriptor.
                pvd_sector = sector
                break

            if vd_type == 255:
                # Terminator.
                break

        if pvd_sector is None:
            raise Exception('Could not find primary volume descriptor')

        self.pvd_sector = pvd_sector

        # Get volume information from the primary volume descriptor.
        #
        # (http://wiki.osdev.org/ISO_9660#The_Primary_Volume_Descriptor)

        volume_info = OrderedDict()
        volume_info['System'] = self.unpack('iso_string', 8, 32, pvd_sector)
        volume_info['Name'] = self.unpack('iso_string', 40, 32, pvd_sector)
        volume_info['Set'] = self.unpack('iso_string', 190, 128, pvd_sector)
        volume_info['Publisher'] = self.unpack('iso_string', 318, 128, pvd_sector)
        volume_info['Data preparer'] = self.unpack('iso_string', 446, 128, pvd_sector)
        volume_info['Application'] = self.unpack('iso_string', 574, 128, pvd_sector)

        volume_info['Creation date'] = self.unpack('iso_date_string', 813, 17, pvd_sector)
        volume_info['Modification date'] = self.unpack('iso_date_string', 830, 17, pvd_sector)
        volume_info['Start date'] = self.unpack('iso_date_string', 864, 17, pvd_sector)
        volume_info['Expiration date'] = self.unpack('iso_date_string', 847, 17, pvd_sector)

        self.info['Volume'] = volume_info

        # TODO: this is pretty horrible, refactor
        extract_dir = None
        directory_times = []
        if config.extract is not None:
            extract_dir = os.path.join(config.extract, volume_info['Name'], self.track_name)
            os.makedirs(extract_dir, exist_ok=True)

        file_info = OrderedDict()

        for file in self.files():
            if file['name'] == '':
                continue

            contents = self.read(0, file['size'], file['sector'])
            file['crc32'] = '{:08x}'.format(crc32(contents))

            if config.extract is not None:
                path = os.path.join(extract_dir, file['path'].lstrip('/'))
                if file['is_directory']:
                    os.makedirs(path, exist_ok=True)

                    if isinstance(file['date'], datetime):
                        # Save the directory modification time for later. If wew were to set it now,
                        # it would be overridden by extracting files that are within it.
                        timestamp = file['date'].timestamp()
                        directory_times.append((path, timestamp))

                if not file['is_directory']:
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                    if self.track_name:
                        display_name = ' '+self.track_name
                    else:
                        display_name = ''

                    print_status('Extracting{}: {:<80}   '.format(display_name, file['path']))

                    with open(path, "wb") as f:
                        f.write(contents)

                        if isinstance(file['date'], datetime):
                            timestamp = file['date'].timestamp()
                            os.utime(path, (timestamp, timestamp))

            file_info[file['path']] = file

        if config.extract is not None:
            print_status("\n")
            for path, timestamp in directory_times:
                os.utime(path, (timestamp, timestamp))

        self.info['Files'] = {'type': 'file_list', 'value': file_info}

        if not config.skip_sector_errors:
            sector_errors = self.find_sector_errors()
            if sector_errors:
                self.info['Errors'] = sector_errors

    def sectors(self):
        for _, file_start, file_stop in self.file.ranges():
            sector_start = file_start // self.sector_size
            sector_stop = file_stop // self.sector_size

            yield from range(sector_start, sector_stop)

    def sector_count(self):
        return len(self.file) // self.sector_size

    def find_sector_errors(self):
        errors = defaultdict(list)

        n_p = n_q = n_edc = 0

        for i, sector in enumerate(self.sectors()):
            p, q, edc = self.check_errors(sector)
            if not p:
                errors[sector].append('p')
                n_p += 1

            if not q:
                errors[sector].append('q')
                n_q += 1

            if not edc:
                errors[sector].append('edc')
                n_edc += 1

            # Because this is so slow, show a status line.
            if not i & 0x7f or i == self.sector_count()-1:
                print_status('Checking sector {} of {} ({:.2f}%)... found {} P errors, {} Q errors, {} EDC errors   '.format(
                    i+1, self.sector_count(), (i+1)/self.sector_count()*100, n_p, n_q, n_edc))

        print_status('\n')  # Print newlines.

        return errors

    def read_raw(self, offset, size):
        return super().read(offset, size)

    def read(self, offset, size, sector=0, raw=False):
        if raw:
            offset = offset + sector * self.sector_size
            return self.read_raw(offset, size)

        # Walk to the actual sector. Sectors can have
        # different sizes so we can't just calculate this.
        sector_no = sector
        while offset > self.data_size(sector_no):
            offset -= self.data_size(sector_no)
            sector_no += 1

        chunks = []
        while size > 0:
            sector = self.read_sector(sector_no)
            chunk_size = min(self.data_size(sector_no)-offset, size)

            chunks.append(sector[offset:offset+chunk_size])

            sector_no += 1
            size -= chunk_size
            offset = 0

        return b''.join(chunks)

    def read_sector(self, sector, raw=False):
        if raw:
            return self.read_raw(sector*self.sector_size, self.sector_size)

        else:
            return self.read_raw(sector * self.sector_size + self.data_offset, self.data_size(sector))

    def unpack(self, value_type, offset, size, sector, raw=False):
        format_dict = {
            'uint8': 'B',
            'uint16': 'H',
            'uint32': 'I',
            'int8': 'b',
            'int16': 'h',
            'int32': 'i',
        }

        value = self.read(offset, size, sector, raw=raw)

        if value_type in format_dict:
            fmt = format_dict[value_type]
            return struct.unpack(fmt, value)[0]

        elif value_type == 'iso_date_string':
            # dec-datetime
            # http://wiki.osdev.org/ISO_9660#Date.2Ftime_format
            if value == b'0000000000000000\x00':
                return ''

            try:
                dt = datetime.strptime(value[:14].decode('ascii'), '%Y%m%d%H%M%S')

                hundredths = int(value[14:16].decode('ascii'))
                dt += timedelta(milliseconds=hundredths*10)
                # tz = value[16]  # TODO

                return dt

            except ValueError:
                # some dates are malformed
                value = value.decode('ascii')
                value = re.sub('\W', '.', value)

                dt = '{}-{}-{} {}:{}:{}'.format(value[0:4], value[4:6], value[6:8],
                                                value[8:10], value[10:12], value[12:14])

                return dt

        elif value_type == 'iso_string':
            # strA and strD
            # http://wiki.osdev.org/ISO_9660#String_format
            return value.decode('ascii').strip()

        elif value_type == 'string':
            return value.decode('ascii')

    def files(self, sector=None, size=None, path=''):
        offset = 0
        if sector is None:
            # Root directory record.
            sector = self.pvd_sector
            offset = 156

        else:
            # Skip self and parent records.
            r_self = self.unpack_record(offset, sector)
            offset += r_self['record_size']

            parent = self.unpack_record(offset, sector)
            offset += parent['record_size']

        size_left = size
        while size is None or offset < size_left:
            record = self.unpack_record(offset, sector)

            if record['record_size'] == 0:
                if size is not None:
                    size_left -= self.data_size(sector)
                offset = 0
                sector += 1
                continue

            if sector != self.pvd_sector:
                record['path'] = path + '/' + record['name']

            else:
                record['path'] = path

            yield record

            if record['is_directory']:
                yield from self.files(sector=record['sector'], size=record['size'], path=record['path'])

            offset += record['record_size']

            if sector == self.pvd_sector:
                break

    def unpack_record(self, offset, sector):
        record = {}

        record['record_size'] = self.unpack('uint8', offset+0, 1, sector)
        if record['record_size'] == 0:
            return record

        record['sector'] = self.unpack('uint32', offset+2, 4, sector) - self.sector_offset
        record['size'] = self.unpack('uint32', offset+10, 4, sector)

        flag_bits = self.unpack('uint8', offset+25, 1, sector)
        flags = {0: 'is_hidden', 2: 'is_directory', 4: 'is_associated', 8: 'has_extended_format',
                 16: 'has_extended_permissions', 128: 'is_not_final'}
        for binary, text in flags.items():
            if flag_bits & binary:
                record[text] = True
            elif text == 'is_directory':
                record[text] = False

        # Record datetime.
        kwargs = {
            'year': self.unpack('uint8', offset+18, 1, sector)+1900,
            'month': self.unpack('uint8', offset+19, 1, sector),
            'day': self.unpack('uint8', offset+20, 1, sector),
            'hour': self.unpack('uint8', offset+21, 1, sector),
            'minute': self.unpack('uint8', offset+22, 1, sector),
            'second': self.unpack('uint8', offset+23, 1, sector),
        }
        record['date'] = datetime(**kwargs)  # TODO timezone

        name_size = self.unpack('uint8', offset+32, 1, sector)
        name = self.unpack('iso_string', offset+33, name_size, sector)

        if name == '\x00':
            name = ''
        record['name'] = name.replace(';1', '')

        return record

    def ecc(self, sector):
        """
        Check consistency of error correction P-vectors. The i-th P-vector is defined as
        [S[i], S[86+i], S[86*2+i], ..., S[86*23+i]] and the i-th P code is [S[86*24+i], P[86*25+i]].

        The i-th Q-vector is defined as [S[i/2*86 % 2236 + i%2], S[(i/2*86+88) % 2236 + i%2], ...,
        S[(i/2*86+88*43) % 2236 + i%2]], with the i-th Q code being [S[86*2+i], S[86*2+i+52]].

        Source: ECMA-130, Annex A.

        :param sector:
        :return:
        """
        ecc_p = [0]*2*86
        ecc_q = [0]*2*52

        sector_data = self.read_sector(sector, raw=True)

        if self.format == 'mode2':
            sector_data = (b'\x00'*16)+sector_data[16:]

        # P vectors
        for major in range(86):
            indexes = [major + minor*86 for minor in range(24)]
            msg = [sector_data[0x0c + index] for index in indexes]

            a, b = self.rs_encode(msg)
            ecc_p[major+0] = a
            ecc_p[major+86] = b

        # Q vectors
        for major in range(52):
            indexes = [(minor*88 + major//2*86) % (52*43) + (major & 1) for minor in range(43)]
            msg = [sector_data[0x0c + index] for index in indexes]

            a, b = self.rs_encode(msg)
            ecc_q[major+0] = a
            ecc_q[major+52] = b

        return ecc_p, ecc_q

    def check_errors(self, sector):
        edc_valid = ecc_p_valid = ecc_q_valid = True

        if self.edc_offset(sector) is not None:
            sector_edc = self.unpack('uint32', self.edc_offset(sector), 4, sector, raw=True)

            edc_valid = (sector_edc == 0 or self.edc(sector) == sector_edc)

        if self.ecc_offset(sector) is not None:
            sector_ecc_p = self.read(self.ecc_offset(sector), 86*2, sector, raw=True)
            sector_ecc_q = self.read(self.ecc_offset(sector) + 86*2, 52*2, sector, raw=True)

            ecc_p, ecc_q = self.ecc(sector)

            ecc_p_valid = (bytes(ecc_p) == sector_ecc_p)
            ecc_q_valid = (bytes(ecc_q) == sector_ecc_q)

        return ecc_p_valid, ecc_q_valid, edc_valid


    @staticmethod
    def rs_encode(msg):
        """
        Reed-Solomon over the GF(2^8) field, generated over the primitive polynomial P(x) = x^8 + x^4 + x^3 + x^2 + 1,
        represented in hex by 0x11d, with primitive element a = 2.

        The code is 2 bytes long, thus the generator polynomial is given by (x-a^0)(x-a^1) = (x-1)(x-2) = x^2 - 3x + 2.
        Because the generator is small, we can simplify the polynomial division significantly. Multiplying by 2 and 3
        is straightforward, therefore we can get away with much simpler multiplication.

        Source: ECMA-130, Annex A.
        See also: https://en.wikiversity.org/wiki/Reed–Solomon_codes_for_coders
                  https://research.swtch.com/field
                  https://github.com/tomerfiliba/reedsolomon
                  iso2bin, EdcEcc.cpp
                  ecm by Neill Corlett


        :param msg:
        :return:
        """

        def gf_mul2(x):
            """Multiply value by 2 in GF(2^8)."""
            y = x << 1

            if y & 0x100:
                y ^= 0x11d

            return y

        # Polynomial division of m_0*x^n + m_1*x^(n_1) + ... + m_n*x^0 by the generator polynomial x^2 + 3x + 2.
        # The generator coefficients are [1, 3, 2]. We can skip the first coefficient, as it would serve to zero out
        # the left side of the quotient, which we don't care about, because we only want the remainder. For clarity,
        # we unroll the inner loop, instead explicitly subtracting in a polynomial division step.
        # The resulting remainder is the RS code.
        msg = bytearray(msg) + b'\x00\x00'  # Extend the message by the remainder.

        for i in range(len(msg)-2):
            coef = msg[i]
            if coef:
                msg[i+1] ^= gf_mul2(coef) ^ coef  # m(i+1) -= 3 * m(i)
                msg[i+2] ^= gf_mul2(coef)         # m(i+2) -= 2 * m(i)

        return [msg[-2], msg[-1]]


    def edc(self, sector):
        """
        The EDC code is a 32-bit CRC with polynomial P(x) = (x^16 + x^15 + x^2 + 1)(x^16 + x^2 + x + 1),
        represented by 0xd8018001 in hex.

        Original algorithm by Gary S. Brown, used by permission.

        Source: ECMA-130, 14.3 (EDC field).
        See also: https://en.wikipedia.org/wiki/Cyclic_redundancy_check
                  http://www.ross.net/crc/download/crc_v3.txt
                  http://www.hackersdelight.org/hdcodetxt/crc.c.txt


        :param sector:
        :return:
        """
        sector_data = self.read(offset=self.skip_offset,
                                size=self.edc_offset(sector)-self.skip_offset,
                                sector=sector, raw=True)

        if self._edc_table is None:
            # Generate table
            self._edc_table = [0]*256

            for i in range(256):
                crc = i
                for j in range(8):
                    subtract = crc & 1
                    crc >>= 1
                    if subtract:
                        crc ^= 0xd8018001

                self._edc_table[i] = crc


        edc = 0
        for byte in sector_data:
            edc = (edc >> 8) ^ self._edc_table[(edc ^ byte) & 0xff]

        return edc







