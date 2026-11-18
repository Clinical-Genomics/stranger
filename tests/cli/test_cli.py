import json

from click.testing import CliRunner

from stranger.cli import cli


def test_stranger_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_stranger_cli(vcf_path):
    runner = CliRunner()
    result = runner.invoke(cli, [vcf_path])
    assert result.exit_code == 0


def test_stranger_cli_zipped(vcf_zipped_path):
    runner = CliRunner()
    result = runner.invoke(cli, [vcf_zipped_path])
    assert result.exit_code == 0


def test_stranger_trgt(vcf_trgt_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["--trgt", vcf_trgt_path])
    assert result.exit_code == 0


def test_stranger_trgt_dot_mc(vcf_trgt_path_dot_mc):
    runner = CliRunner()
    result = runner.invoke(cli, ["--trgt", vcf_trgt_path_dot_mc])
    assert result.exit_code == 0


def test_stranger_trgt_info_values(vcf_trgt_path, tmp_path):
    """Test that list and free text catalog annotations give valid INFO values and headers"""
    # GIVEN a catalog with a list PathologicStruc and InheritanceMode, and free text with
    # spaces and commas, for a locus in the TRGT VCF
    catalog = [
        {
            "LocusId": "DAB1",
            "TRID": "SCA37_DAB1",
            "NormalMax": 10,
            "PathologicMin": 31,
            "PathologicStruc": [0, 1],
            "InheritanceMode": ["AD", "AR"],
            "Disease": "Spinocerebellar ataxia, type 37",
            "SourceDisplay": "Seixas et al 2017, Am J Hum Genet",
            "HGNCId": 2661,
        }
    ]
    repeats_file = tmp_path / "catalog.json"
    repeats_file.write_text(json.dumps(catalog))

    # WHEN annotating the TRGT VCF
    runner = CliRunner()
    result = runner.invoke(cli, ["--trgt", "-f", str(repeats_file), vcf_trgt_path])
    assert result.exit_code == 0

    # THEN the list annotations are declared as lists
    lines = result.output.splitlines()
    headers = [line for line in lines if line.startswith("##INFO")]
    assert (
        '##INFO=<ID=PathologicStruc,Number=.,Type=Integer,Description="Struc components counting'
        ' towards pathogenicity as motif numbers">' in headers
    )
    assert any(header.startswith("##INFO=<ID=InheritanceMode,Number=.,") for header in headers)

    # AND the annotated variants have comma separated lists and percent-encoded free text
    infos = [line.split("\t")[7] for line in lines if "TRID=SCA37_DAB1" in line]
    assert infos
    for info in infos:
        annotations = dict(entry.split("=", 1) for entry in info.split(";") if "=" in entry)
        assert annotations["PathologicStruc"] == "0,1"
        assert annotations["InheritanceMode"] == "AD,AR"
        assert annotations["Disease"] == "Spinocerebellar%20ataxia%2C%20type%2037"
        assert annotations["SourceDisplay"] == "Seixas%20et%20al%202017%2C%20Am%20J%20Hum%20Genet"
        assert annotations["HGNCId"] == "2661"
        # AND there is no whitespace in the INFO field
        assert " " not in info
        # AND every INFO key is declared in the header
        header_ids = {header.split("ID=", 1)[1].split(",", 1)[0] for header in headers}
        assert set(entry.split("=", 1)[0] for entry in info.split(";")) <= header_ids
