import logging
from pprint import pprint as pp

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
@click.pass_context
def cli(context, repeats_file):
    """Table print repeat info"""

    repeat_information = {}
    with open(repeats_file, "r") as file_handle:
        repeat_information = parse_repeat_file(file_handle, repeats_file_type="json")

    if not repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    header = [
        "HGNCId",
        "LocusId",
        "DisplayRU",
        "InheritanceMode",
        "normal_max",
        "pathologic_min",
        "Disease",
        "SourceDisplay",
        "SourceId",
    ]
    table_line = "| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} |"
    click.echo(
        table_line.format(
            header[0],
            header[1],
            header[2],
            header[3],
            header[4],
            header[5],
            header[6],
            header[7],
            header[8],
        )
    )
    click.echo(
        table_line.format(
            "-------",
            "-------",
            "-------",
            "-------",
            "-------",
            "-------",
            "-------",
            "-------",
            "-------",
        )
    )
    for entry in repeat_information:
        click.echo(
            table_line.format(
                repeat_information[entry][header[0]],
                entry,
                repeat_information[entry][header[2]],
                repeat_information[entry][header[3]],
                repeat_information[entry][header[4]],
                repeat_information[entry][header[5]],
                repeat_information[entry][header[6]],
                repeat_information[entry][header[7]],
                repeat_information[entry][header[8]],
            )
        )


if __name__ == "__main__":
    cli()
