import pytest

from stranger.utils import decompose_var, get_trgt_repeat_res, parse_repeat_file


def test_parse_repeat_file(repeats_file_handle):
    ## GIVEN a file handle with repeat lines
    ## WHEN parsing the repeat info
    repeats_info = parse_repeat_file(repeats_file_handle)

    ## THEN assert that there are some repeat info returned
    assert repeats_info


def test_parse_repeat_json_file(repeats_json_handle):
    ## GIVEN a file handle with repeat json lines
    ## WHEN parsing the repeat info json
    repeats_info = parse_repeat_file(repeats_json_handle, "json")

    ## THEN assert that some repeat info was returned
    assert repeats_info


def test_parse_repeat_line():
    ## GIVEN a some repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1	ATXN1	CAG	35	45	SCA1",
    ]
    ## WHEN parsing the repeat info
    repeats_info = parse_repeat_file(repeats_info_lines)

    ## THEN assert that the expected repeat info is there
    assert "ATXN1" in repeats_info
    ## THEN assert that the hgnc_id is there
    assert repeats_info["ATXN1"]["hgnc_id"] == 10548
    assert repeats_info["ATXN1"]["hgnc_symbol"] == "ATXN1"
    assert repeats_info["ATXN1"]["repid"] == "ATXN1"
    assert repeats_info["ATXN1"]["ru"] == "CAG"
    assert repeats_info["ATXN1"]["normal_max"] == 35
    assert repeats_info["ATXN1"]["pathologic_min"] == 45
    assert repeats_info["ATXN1"]["disease"] == "SCA1"


def test_parse_malformaed_repeat_line():
    ## GIVEN a some malformed repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1",
    ]
    ## WHEN parsing the repeat info
    ## THEN assert that an exception is raised
    with pytest.raises(SyntaxError):
        repeats_info = parse_repeat_file(repeats_info_lines)


def test_parse_malformaed_repeat_line_wrong_value():
    ## GIVEN a some malformed repeat info lines
    repeats_info_lines = [
        "#hgnc_id	hgnc_symbol	repid	ru	normal_max	pathologic_min	disease",
        "10548	ATXN1	ATXN1	CAG	hello	45	SCA1",
    ]
    ## WHEN parsing the repeat info
    ## THEN assert that an exception is raised
    with pytest.raises(ValueError):
        repeats_info = parse_repeat_file(repeats_info_lines)


def test_get_trgt_repeat_res(repeats_json_handle):
    # GIVEN repeats info from a JSON file
    repeats_info = parse_repeat_file(repeats_json_handle, "json")

    # GIVEN that the parsing returns a set pathologic_struc
    assert repeats_info["HTT"]["PathologicStruc"]
    assert repeats_info["HTT"]["pathologic_struc"] == [0]

    # GIVEN a variant
    variant_info = {
        "info_dict": {
            "TRID": "HTT",
            "END": "3074966",
            "MOTIFS": "CAG,CCG",
            "STRUC": "(CAG)nCAACAG(CCG)n",
            "FOUND_IN": "TRGT",
        },
        "format_dicts": [{"MC": "27_9, 32_9"}],
    }

    # WHEN parsing repeat results

    repeat_res = get_trgt_repeat_res(variant_info, repeats_info)
    assert repeat_res == [27, 32]


def test_get_trgt_repeat_res_single_mc(repeats_json_handle):
    # GIVEN repeats info from a JSON file
    repeats_info = parse_repeat_file(repeats_json_handle, "json")

    # GIVEN that the parsing returns a set pathologic_struc
    assert repeats_info["HTT"]["PathologicStruc"]
    assert repeats_info["HTT"]["pathologic_struc"] == [0]

    variant_info = {
        "info_dict": {
            "TRID": "HTT",
            "END": "3074966",
            "MOTIFS": "CAG,CCG",
            "STRUC": "(CAG)nCAACAG(CCG)n",
            "FOUND_IN": "TRGT",
        },
        "format_dicts": [{"MC": "27_9"}],
    }

    repeat_res = get_trgt_repeat_res(variant_info, repeats_info)
    assert repeat_res == [27]


def test_single_value_format_fields():
    # GIVEN a variant with multiple ALT alleles and some single-value FORMAT fields
    variant_info = {
        "alts": ["A", "C"],
        "format_dicts": [{"AL": "54,54", "GT": "1/2", "PS": ".", "SDP": "5"}],
    }

    # WHEN decomposing the variant
    decomposed = decompose_var(variant_info)

    # THEN assert that the decomposition is correct
    assert len(decomposed) == 2

    # THEN check GT decomposition
    gts = [variant["format_dicts"][0]["GT"] for variant in decomposed]
    assert gts == ["1/.", "./1"]

    # THEN check that single-value fields are preserved
    for decomposed_variant in decomposed:
        first_sample_format = decomposed_variant["format_dicts"][0]
        assert first_sample_format["AL"] == "54"
        assert first_sample_format["PS"] == "."
        assert first_sample_format["SDP"] == "5"


def test_phased_gt():
    # Given a variant with phased GT
    variant_info = {
        "alts": ["A", "C"],
        "format_dicts": [
            {
                "GT": "1|2",
            }
        ],
    }

    # WHEN decomposing the variant
    decomposed = decompose_var(variant_info)

    # THEN assert we have phased GTs after decomposition
    gts = [variant["format_dicts"][0]["GT"] for variant in decomposed]
    assert gts == ["1|.", ".|1"]
