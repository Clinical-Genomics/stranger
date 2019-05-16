import logging
import coloredlogs
import click
import gzip

from pprint import pprint as pp
from codecs import (open, getreader)

from stranger.resources import repeats_json_path
from stranger.utils import (parse_repeat_file, get_repeat_info, get_info_dict, get_variant_line)
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
    default=repeats_json_path,
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
    LOG.info("Running stranger version %s", __version__)

    repeat_information = None
    repeats_file_type = 'tsv'
    if repeats_file.endswith('.json'):
        repeats_file_type = 'json'
    LOG.info("Parsing repeats file %s", repeats_file)

    with open(repeats_file, 'r') as file_handle:
        repeat_information = parse_repeat_file(file_handle, repeats_file_type)

    if not repeat_information:
        LOG.warning("Could not find any repeat info")
        context.abort()

    stranger_info = 'STR_STATUS'
    stranger_description = "Repeat expansion status. Alternatives in [normal, pre_mutation, full_mutation]"
    stranger_header = '##INFO=<ID={0},Number={1},Type={2},Description="{3}">'.format(
        stranger_info, 'A', 'String', stranger_description
    )

    if vcf.endswith('.gz'):
        LOG.info("Vcf is zipped")
        vcf_handle = getreader('utf-8')(gzip.open(vcf), errors='replace')
    else:
        vcf_handle = open(vcf, mode='r', encoding='utf-8', errors='replace')

    LOG.info("Parsing variants from %s", vcf)
    for line in vcf_handle:
        line = line.rstrip()
        if line.startswith('#'):
            if line.startswith('##'):
                click.echo(line)
                continue
            # Print the new header line describing stranger annotation
            click.echo(stranger_header)
            # Print the vcf header line
            header_info = line[1:].split('\t')
            click.echo(line)
            continue
        variant_info = dict(zip(header_info, line.split('\t')))
        variant_info['alts'] = variant_info['ALT'].split(',')
        variant_info['info_dict'] = get_info_dict(variant_info['INFO'])
        repeat_string = get_repeat_info(variant_info, repeat_information)
        if repeat_string:
            variant_info['info_dict'][stranger_info] = repeat_string

        click.echo(get_variant_line(variant_info, header_info))
