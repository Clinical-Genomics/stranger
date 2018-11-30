import pytest
from stranger.utils import parse_repeat_file, get_repeat_info


def test_parse_repeat_file(repeats_file_handle):
    ## GIVEN a file handle with repeat lines
    ## WHEN parsing the repeat info
    repeats_info = parse_repeat_file(repeats_file_handle)
    
    ## THEN assert that there are some repeat info returned
    assert repeats_info

def test_parse_repeat_line():
    ## GIVEN a some repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1	ATXN1	CAG	35	45	SCA1"
    ]
    ## WHEN parsing the repeat info
    repeats_info = parse_repeat_file(repeats_info_lines)
    
    ## THEN assert that the expected repeat info is there
    assert 'ATXN1' in repeats_info
    ## THEN assert that the hgnc_id is there
    assert repeats_info['ATXN1']['hgnc_id'] == 10548
    assert repeats_info['ATXN1']['hgnc_symbol'] == 'ATXN1'
    assert repeats_info['ATXN1']['repid'] == 'ATXN1'
    assert repeats_info['ATXN1']['ru'] == 'CAG'
    assert repeats_info['ATXN1']['normal_max'] == 35
    assert repeats_info['ATXN1']['pathologic_min'] == 45
    assert repeats_info['ATXN1']['disease'] == 'SCA1'

def test_parse_malformaed_repeat_line():
    ## GIVEN a some malformed repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1"
    ]
    ## WHEN parsing the repeat info
    ## THEN assert that an exception is raised
    with pytest.raises(SyntaxError):
        repeats_info = parse_repeat_file(repeats_info_lines)

def test_parse_malformaed_repeat_line_wrong_value():
    ## GIVEN a some malformed repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1	ATXN1	CAG	hello	45	SCA1"
    ]
    ## WHEN parsing the repeat info
    ## THEN assert that an exception is raised
    with pytest.raises(ValueError):
        repeats_info = parse_repeat_file(repeats_info_lines)
