import logging

from pprint import pprint as pp

import coloredlogs
import click

from cyvcf2 import VCF

from stranger.resources import repeats_path
from stranger.utils import parse_repeat_file, get_repeat_info
from stranger.vcf_utils import print_headers
from stranger.__version__ import __version__

LOG = logging.getLogger(__name__)
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

@click.command()
@click.argument('vcf')
@click.option('-f', '--repeats-file',
    type = click.Path(exists=True),
    help="Path to a file with repeat definitions. See README for explanation",
    default=repeats_path,
    show_default=True,
)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS),
              help="Set the level of log output.", show_default=True)
@click.pass_context
def cli(context, vcf, repeats_file, loglevel):
    """Annotate str variants with str status"""
    coloredlogs.install(level=loglevel)

    header_string = 'STR_STATUS'
    repeat_information = None
    with open(repeats_file, 'r') as file_handle:
        repeat_information = parse_repeat_file(file_handle)

    if not repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    vcf_obj = VCF(vcf)
    vcf_obj.add_info_to_header(
        {
            "ID": header_string,
            "Number": 'A',
            "Type": "String",
            "Description": "Repeat expansion status. Alternatives in ['normal', 'pre_mutation', 'full_mutation']"
        }
    )
    
    print_headers(vcf_obj)

    for var in vcf_obj:
        repeat_string = get_repeat_info(var, repeat_information)
        if repeat_string:
            var.INFO[header_string] = repeat_string
        click.echo(str(var).rstrip())
