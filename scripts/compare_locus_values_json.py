import logging

import coloredlogs
import requests

LOG = logging.getLogger(__name__)
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

import click

from stranger.resources import repeats_path
from stranger.utils import get_repeat_info, parse_repeat_file


@click.command()
@click.option(
    "-f",
    "--repeats-file",
    type=click.Path(exists=True),
    help="Path to a file with repeat definitions. See README for explanation",
    default=repeats_path,
    show_default=True,
)
@click.option(
    "-x",
    "--alt-repeats-file",
    type=click.Path(exists=True),
    help="Path to a second file with repeat definitions. See README for explanation",
    default=repeats_path,
    show_default=True,
)
@click.option(
    "--loglevel",
    default="INFO",
    type=click.Choice(LOG_LEVELS),
    help="Set the level of log output.",
    show_default=True,
)
@click.pass_context
def cli(context, repeats_file, alt_repeats_file, loglevel):
    """Test if values differ between loci for variant catalog jsons"""
    coloredlogs.install(level=loglevel)
    with open(repeats_file, "r") as file_handle:
        repeat_information = parse_repeat_file(file_handle, repeats_file_type="json")

    with open(alt_repeats_file, "r") as file_handle:
        other_repeat_information = parse_repeat_file(file_handle, repeats_file_type="json")

    if not repeat_information or not other_repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    for entry in repeat_information:
        for key in repeat_information[entry]:
            if entry not in other_repeat_information:
                LOG.info("Entry %s not found in alt file.", entry)
                continue
            if key not in other_repeat_information[entry]:
                LOG.warning("Entry %s field %s missing in alt file entry.", entry, key)
                continue
            if other_repeat_information[entry][key] != repeat_information[entry][key]:
                LOG.error(
                    "Entry %s field %s differs between file: %s and alt: %s",
                    entry,
                    key,
                    repeat_information[entry][key],
                    other_repeat_information[entry][key],
                )


if __name__ == "__main__":
    cli()
