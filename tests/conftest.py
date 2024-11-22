import pytest

from stranger.resources import repeats_path


@pytest.fixture()
def vcf_path():
    return "tests/fixtures/643594.clinical.str.vcf"


@pytest.fixture()
def vcf_zipped_path():
    return "tests/fixtures/643594.clinical.str.vcf.gz"


@pytest.fixture()
def vcf_trgt_path():
    return "tests/fixtures/sample.trgt.vcf"


@pytest.fixture()
def vcf_trgt_path_dot_mc():
    return "tests/fixtures/HG002_Revio.sort.vcf.gz"


@pytest.fixture()
def repeats_file_handle():
    return open(repeats_path, "r")
