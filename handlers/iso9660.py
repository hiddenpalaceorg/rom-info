"""
Handle ISO 9660 disc image files.

Format reference: http://wiki.osdev.org/ISO_9660
"""
import struct
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from zlib import crc32
import config
from .base_handler import BaseHandler


class ISO9660Handler(BaseHandler):
    def __init__(self, sector_offset=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sector_offset = sector_offset

        self.format = None
        self.sector_size = None
        self.pvd_sector = None

        self._edc_table = None

    def test(self):
        if self._read(0x9311, 5) == b'CD001':
            self.format = 'raw'
            self.sector_size = 2352
            return True

        elif self._read(0x8001, 5) == b'CD001':
            self.format = 'iso'
            self.sector_size = 2048
            return True

        else:
            return False

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

        file_info = OrderedDict()

        for file in self.files():
            if file['name'] == '':
                continue

            contents = self.read(0, file['size'], file['sector'])
            file['crc32'] = '{:08x}'.format(crc32(contents))

            file_info[file['path']] = file

        self.info['Files'] = {'type': 'file_list', 'value': file_info}

        if not config.skip_sector_errors:
            sector_errors = self.find_sector_errors()
            if sector_errors:
                self.info['Errors'] = sector_errors

    def find_sector_errors(self):
        errors = defaultdict(list)

        n_p = n_q = n_edc = 0
        n_sectors = len(self.file)//2352

        for i in range(n_sectors):
            p, q, edc = self.check_errors(i)
            if not p:
                errors[i].append('p')
                n_p += 1

            if not q:
                errors[i].append('q')
                n_q += 1

            if not edc:
                errors[i].append('edc')
                n_edc += 1

            # Because this is so slow, show a status line.
            if not i & 0x7f or i == n_sectors-1:
                print('\rChecking sector {} of {} ({:.2f}%)... found {} P errors, {} Q errors, {} EDC errors   '.format(
                    i+1, n_sectors, (i+1)/n_sectors*100, n_p, n_q, n_edc), end=" ")

        print('\n')  # Print newlines.

        return errors

    def _read(self, offset, size):
        return super().read(offset, size)

    def read(self, offset=None, size=None, sector=0):
        if size is None:
            raise Exception("You must specify size.")

        if offset is None:
            raise Exception("You must specify an offset.")

        sector_no = sector + offset//2048
        offset = offset % 2048

        chunks = []
        while size > 0:
            sector = self.read_sector(sector_no)
            chunk_size = min(2048-offset, size)

            chunks.append(sector[offset:offset+chunk_size])

            sector_no += 1
            size -= chunk_size
            offset = 0

        return b''.join(chunks)

    def read_sector(self, sector_no):
        if self.format == 'raw':
            return self._read(sector_no*self.sector_size + 0x10, 2048)

        elif self.format == 'iso':
            return self._read(sector_no*self.sector_size, 2048)

    def unpack(self, value_type, offset, size, sector):
        format_dict = {
            'uint8': 'B',
            'uint16': 'H',
            'uint32': 'I',
            'int8': 'b',
            'int16': 'h',
            'int32': 'i',
        }

        value = self.read(offset, size, sector)

        if value_type in format_dict:
            fmt = format_dict[value_type]
            return struct.unpack(fmt, value)[0]

        elif value_type == 'iso_date_string':
            # dec-datetime
            # http://wiki.osdev.org/ISO_9660#Date.2Ftime_format
            if value == b'0000000000000000\x00':
                return ''

            dt = datetime.strptime(value[:14].decode('ascii'), '%Y%m%d%H%M%S')

            hundredths = int(value[14:16].decode('ascii'))
            dt += timedelta(milliseconds=hundredths*10)
            # tz = value[16]  # TODO

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

        while size is None or offset < size:
            record = self.unpack_record(offset, sector)

            if record['record_size'] == 0:
                break

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

        sector_data = self._read(sector*2352, 2352)

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
        sector_edc = int.from_bytes(self._read(sector*2352+0x810, 4), byteorder='little')
        sector_ecc_p = self._read(sector*2352+0x81c, 86*2)
        sector_ecc_q = self._read(sector*2352+0x81c+86*2, 52*2)

        ecc_p, ecc_q = self.ecc(sector)

        ecc_p_valid = (bytes(ecc_p) == sector_ecc_p)
        ecc_q_valid = (bytes(ecc_q) == sector_ecc_q)
        edc_valid = (self.edc(sector) == sector_edc)

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
        sector_data = self._read(sector*2352, 0x810)

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







