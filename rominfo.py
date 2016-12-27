#!/usr/bin/env python3
import config
from analyze import analyze_file
from utils import MmappedFile


def main(args=None):
    config.parse_args(args=args)

    for filename in config.files:
        with MmappedFile(filename) as file:
            analyze_file(file, filename)


if __name__ == "__main__":
    main()
