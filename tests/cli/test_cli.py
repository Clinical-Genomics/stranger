from stranger.cli import cli

from click.testing import CliRunner

def test_stranger_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0

def test_stranger_cli(vcf_path):
    runner = CliRunner()
    result = runner.invoke(cli, [vcf_path])
    assert result.exit_code == 0

def test_stranger_cli_zipped(vcf_zipped_path):
    runner = CliRunner()
    result = runner.invoke(cli, [vcf_zipped_path])
    assert result.exit_code == 0