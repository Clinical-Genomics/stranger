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
