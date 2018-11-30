import logging

from parse import parse

LOG = logging.getLogger(__name__)

def parse_repeat_file(file_handle):
    """Parse a file with information about the repeats
    
    Args:
        file_handle(iterable(str))
    
    Returns:
        repeat_info(dict)
    """
    repeat_info = {}
    header = []
    for i,line in enumerate(file_handle,1):
        if not len(line) > 1:
            continue
        line = line.rstrip()
        if line.startswith('#'):
            if not line.startswith('##'):
                header = line[1:].split('\t')
            continue
        line = line.split('\t')
        if not len(line) == len(header):
            LOG.warning('\t'.join(line))
            raise SyntaxError("Line {0} is malformed".format(i))
        repeat = dict(zip(header, line))
        try:
            repeat['hgnc_id'] = int(repeat['hgnc_id'])
            repeat['normal_max'] = int(repeat['normal_max'])
            repeat['pathologic_min'] = int(repeat['pathologic_min'])
        except ValueError as err:
            LOG.warning("Line %s is malformed",i)
            LOG.warning('\t'.join(line))
            raise err
        repeat_info[repeat['repid']] = repeat

    return repeat_info

def get_repeat_info(variant, repeat_info):
    """Find the correct mutation level of a str variant
    
    Args:
        variant(cyvcf2.variant)
        repeat_info(dict)
    
    Returns:
        info_string(str)
    """
    repeat_strings = []
    # There can be one or two alternatives
    alleles = variant.ALT
    repeat_id = variant.INFO.get('REPID')
    if not repeat_id in repeat_info:
        LOG.warning("No info for repeat id %s", repeat_id)
        return None
    rep_lower = repeat_info[repeat_id]['normal_max']
    rep_upper = repeat_info[repeat_id]['pathologic_min']
    for allele in alleles:
        repeat_res = parse("<STR{:d}>", allele)
        if not repeat_res:
            LOG.warning("Allele information is not on correct format: %s", allele)
            raise SyntaxError("Allele on wrong format")
        repeat_number = repeat_res.fixed[0]
        if repeat_number <= rep_lower:
            repeat_strings.append('normal')
        elif repeat_number <= rep_upper:
            repeat_strings.append('pre_mutation')
        else:
            repeat_strings.append('full_mutation')

    return ','.join(repeat_strings)
