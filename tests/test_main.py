import pytest
from rominfo import main


def test_help(capsys):
    with pytest.raises(SystemExit):
        main(['-h'])

    out, err = capsys.readouterr()

    assert 'optional arguments' in out


def test_no_file_specified(capsys):
    with pytest.raises(SystemExit):
        main([])

    out, err = capsys.readouterr()

    assert 'the following arguments are required: FILE' in err


def test_file_not_found():
    with pytest.raises(SystemExit) as excinfo:
        main(['file/does/not/exist.bin'])

    assert 'No such file' in str(excinfo.value)
