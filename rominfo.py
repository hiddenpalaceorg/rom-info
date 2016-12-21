#!/usr/bin/env python3
import mmap
import config
from analyze import analyze_file
from utils import open_mmaped


def main():
    config.parse_args()

    for filename in config.files:
        with open_mmaped(filename, 'rb') as file:
            analyze_file(file, filename)


if __name__ == "__main__":
    main()
