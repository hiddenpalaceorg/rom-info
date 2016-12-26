import pytest

import config

from handlers.dreamcast import GDIHandler
from utils import MmappedFile
from analyze import pretty_print


def test_namco_gdi():
    file_name = "namco_museum/disc.gdi"
    with open("namco_museum_output.txt") as f:
        expected_output = f.read()

    config.skip_sector_errors = False

    with MmappedFile(file_name) as file:
        handler = GDIHandler(file=file, file_name=file_name)

        assert handler.test()

        handler.get_info()

        assert pretty_print(handler.info) == expected_output

