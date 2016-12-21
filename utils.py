import mmap


class open_mmaped:
    def __init__(self, *args, mmap_access=mmap.ACCESS_READ, **kwargs):
        self.file = open(*args, **kwargs)
        self.mmap_access = mmap_access

    def __enter__(self):
        self.file.__enter__()
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=self.mmap_access)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mmap.close()

        return self.file.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, name):
        return getattr(self.mmap, name)

    def __getitem__(self, key):
        return self.mmap.__getitem__(key)
