#!/usr/bin/env python3
import mmap
import config
from analyze import analyze_file


def main():
    config.parse_args()

    for filename in config.files:
        with open(filename, 'rb') as file_handle:
            file = mmap.mmap(file_handle.fileno(), 0, access=mmap.ACCESS_READ)
            analyze_file(file, filename)
            file.close()


if __name__ == "__main__":
    main()
