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
    "--loglevel",
    default="INFO",
    type=click.Choice(LOG_LEVELS),
    help="Set the level of log output.",
    show_default=True,
)
@click.pass_context
def cli(context, repeats_file, loglevel):
    """Table print repeat info"""
    coloredlogs.install(level=loglevel)
    with open(repeats_file, "r") as file_handle:
        repeat_information = parse_repeat_file(file_handle, repeats_file_type="json")

    if not repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    # print(repeat_information)

    # header = ["HGNCId", "LocusId", "DisplayRU", "InheritanceMode", "normal_max", "pathologic_min", "Disease", "SourceDisplay", "SourceId"]

    for entry in repeat_information:
        hgnc_id = repeat_information[entry]["HGNCId"]
        locus_symbol = entry.split("_")[0]

        url = "https://rest.genenames.org/search/hgnc_id/" + str(hgnc_id)
        response = requests.get(url, headers={"Accept": "application/json"})

        if not response:
            LOG.warning("Entry {} not found".format(entry))
        # print(response.text)

        response_json = response.json()
        response_rest = response_json["response"]
        if len(response_rest) == 0:
            LOG.warning("Entry {} not found".format(entry))

        if len(response_rest["docs"]) > 1:
            LOG.warning(
                "Entry {} got {} hgnc responses - using first".format(entry, len(response_rest))
            )

        symbol_from_id = response_rest["docs"][0]["symbol"]

        if symbol_from_id == locus_symbol:
            LOG.info("OK locus %s symbol %s", entry, locus_symbol)
        elif symbol_from_id.lower() == locus_symbol.lower():
            LOG.warning("OK locus %s symbol %s but differs in case", entry, locus_symbol)
        else:
            LOG.error(
                "OOOPS locus_symbol %s and symbol %s from HGNC id %i do not match",
                locus_symbol,
                symbol_from_id,
                hgnc_id,
            )


if __name__ == "__main__":
    cli()
