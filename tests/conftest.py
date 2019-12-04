import os
import pytest

from stranger.resources import repeats_path

@pytest.fixture()
def vcf_path():
    return 'tests/fixtures/643594.clinical.str.vcf'

@pytest.fixture()
def vcf_zipped_path():
    return 'tests/fixtures/643594.clinical.str.vcf.gz'

@pytest.fixture()
def repeats_file_handle():
    return open(repeats_path, 'r')
