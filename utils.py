import mmap
import sys


class MmappedFile:
    def __init__(self, file_name, open_mode='rb', mmap_access=mmap.ACCESS_READ, **kwargs):
        try:
            self.file = open(file_name, mode=open_mode, **kwargs)
        except OSError as e:
            raise SystemExit(e)

        self.file_name = file_name
        self.mmap = None
        self.mmap_access = mmap_access

    def __enter__(self):
        self.file.__enter__()
        try:
            self.mmap = mmap.mmap(self.file.fileno(), 0, access=self.mmap_access)
        except ValueError as e:
            if 'mmap length' in str(e) and sys.maxsize < 2**32:
                raise SystemExit('Could not open {}.\n\n'
                                 'This is an issue with 32-bit mmap.'
                                 ' Please install 64-bit Python to handle files this big.'.format(self.file_name))
            else:
                raise SystemExit('Could not open {}: {}', self.file_name, e)
        except OSError as e:
            if e.winerror == 8 and sys.maxsize < 2**32:
                raise SystemExit('Could not open {}.\n\n'
                                 'This is an issue with 32-bit Python/Windows and mmap.'
                                 ' Please install 64-bit Python to handle files this big.'.format(self.file_name))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mmap.close()

        return self.file.__exit__(exc_type, exc_val, exc_tb)

    def __getitem__(self, key):
        return self.mmap.__getitem__(key)

    def ranges(self):
        yield 0, 0, len(self)

    def __len__(self):
        return self.mmap.__len__()


class ConcatenatedFile:
    def __init__(self, file_names, offsets, **kwargs):
        self.file_names = file_names
        self.files = []
        self.offsets = offsets[:]
        self.offsets.sort()

        for file_name in self.file_names:
            file = MmappedFile(file_name, **kwargs)
            self.files.append(file)

    def __enter__(self):
        self.lengths = []

        for file in self.files:
            file.__enter__()

            self.lengths.append(len(file))

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO deal with exc_type, exc_val and exc_tb
        for file in self.files:
            file.__exit__(None, None, None)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if start is None:
                start = 0

            if stop is None:
                stop = self.offsets[-1] + self.lengths[-1]

            # Find start
            found = False
            file_start = file_stop = None

            for file, file_start, file_stop in reversed(list(self.ranges())):
                if start >= file_start:
                    if file_stop < stop:
                        # print(key, self.offsets, self.lengths, offset+length, stop)
                        raise ValueError("Reads must be within a single chunk")

                    found = True
                    break

            if not found:
                raise ValueError("No chunk containing range")

            start = start - file_start
            stop = stop - file_start
            return self.files[file][start:stop:step]

    def ranges(self):
        for i in range(len(self.files)):
            yield i, self.offsets[i], self.offsets[i]+self.lengths[i]

    def __len__(self):
        length = sum(self.lengths)

        return length


def print_status(status):
    print('\r'+status, file=sys.stderr, end=" ")
