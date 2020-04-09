import pytest
from reddrec.validation import valid_username

def test_valid_username():
    # Proper symbols
    assert valid_username('_example-123')
    assert not valid_username('_*example-123')
    assert not valid_username('spaces arent valid')

    # Proper lengths
    assert valid_username('lol')
    assert valid_username('A' * 20)
    assert not valid_username('xD')
    assert not valid_username('A' * 21)
    assert not valid_username('')
