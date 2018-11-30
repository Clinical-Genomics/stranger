import logging

from pprint import pprint as pp

import click

from stranger.resources import repeats_path
from stranger.utils import parse_repeat_file, get_repeat_info

@click.command()
@click.option('-f', '--repeats-file',
    type = click.Path(exists=True),
    help="Path to a file with repeat definitions. See README for explanation",
    default=repeats_path,
    show_default=True,
)
@click.pass_context
def cli(context, repeats_file):
    """Annotate str variants with str status"""

    repeat_information = {}
    with open(repeats_file, 'r') as file_handle:
        repeat_information = parse_repeat_file(file_handle)

    if not repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    header = ["hgnc_id", "hgnc_symbol", "repid", "ru", "normal_max","pathologic_min", "disease"]
    table_line = "| {0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    click.echo(table_line.format(
        header[0], header[1], header[2], header[3], header[4], header[5], header[6] 
    ))
    click.echo(table_line.format('-------', '-------', '-------', '-------', '-------',
                                 '-------', '-------' ))
    for entry in repeat_information:
        click.echo(table_line.format(
            repeat_information[entry][header[0]],
            repeat_information[entry][header[1]],
            repeat_information[entry][header[2]],
            repeat_information[entry][header[3]],
            repeat_information[entry][header[4]],
            repeat_information[entry][header[5]],
            repeat_information[entry][header[6]],
        ))


if __name__=='__main__':
    cli()