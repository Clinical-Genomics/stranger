import pytest

from stranger.resources import repeats_path

@pytest.fixture()
def repeats_file_handle():
    return open(repeats_path, 'r')