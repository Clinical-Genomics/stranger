import logging
import re

NUM = re.compile(r'\d+')

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

def get_repeat_info(variant_info, repeat_info):
    """Find the correct mutation level of a str variant
    
    Args:
        variant_line(str): A vcf variant line
        repeat_info(dict)
    
    Returns:
        info_string(str)
    """
    repeat_strings = []
    # There can be one or two alternatives
    alleles = variant_info['alts']
    repeat_id = variant_info['info_dict'].get('REPID')
    if not repeat_id in repeat_info:
        LOG.warning("No info for repeat id %s", repeat_id)
        return None

    rep_lower = repeat_info[repeat_id]['normal_max']
    rep_upper = repeat_info[repeat_id]['pathologic_min']
    for allele in alleles:
        if allele == '.':
            repeat_res = [0]
        else:
            repeat_res = [int(num) for num in NUM.findall(allele)]
        if not repeat_res:
            LOG.warning("Allele information is not on correct format: %s", allele)
            raise SyntaxError("Allele on wrong format")
        repeat_number = repeat_res[0]
        if repeat_number <= rep_lower:
            repeat_strings.append('normal')
        elif repeat_number <= rep_upper:
            repeat_strings.append('pre_mutation')
        else:
            repeat_strings.append('full_mutation')

    return ','.join(repeat_strings)

def get_info_dict(info_string):
    """Convert a info string to a dictionary
    
    Args:
        info_string(str): A string that contains the INFO field from a vcf variant
    
    Returns:
        info_dict(dict): The input converted to a dictionary
    """
    info_dict = {}
    if not info_string:
        return info_dict
    if info_string == '.':
        return info_dict
    
    for annotation in info_string.split(';'):
        splitted_annotation = annotation.split('=')
        key = splitted_annotation[0]
        if len(splitted_annotation) == 1:
            info_dict[key] = None
            continue
        value = splitted_annotation[1]
        info_dict[key] = value
    
    return info_dict

def get_variant_line(variant_info, header_info):
    """Convert variant dictionary back to a VCF formated string
    
    Args:
        variant_info(dict):
        header_info(list)
    
    Returns:
        variant_string(str): VCF formated variant
    """
    
    info_dict = variant_info['info_dict']
    if not info_dict:
        info_string = '.'
    else:
        info_list = []
        for annotation in info_dict:
            if info_dict[annotation] is None:
                info_list.append(annotation)
                continue
            info_list.append('='.join([annotation, info_dict[annotation]]))
        variant_info['INFO'] = ';'.join(info_list)
    
    variant_list = []
    for annotation in header_info:
        variant_list.append(variant_info[annotation])
    
    return '\t'.join(variant_list)