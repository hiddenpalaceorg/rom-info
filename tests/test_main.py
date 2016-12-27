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


def test_file_not_found(capsys):
    with pytest.raises(SystemExit):
        main(['file/does/not/exist.bin'])

    out, err = capsys.readouterr()

    assert 'No such file' in err
