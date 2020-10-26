import logging
import re
import yaml

from pprint import pprint as pp

from stranger.constants import RANK_SCORE, ANNOTATE_REPEAT_KEYS

NUM = re.compile(r'\d+')

LOG = logging.getLogger(__name__)

def parse_tsv(file_handle):
    """Parse a repeats file in the tsv file format

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

def parse_json(file_handle):
    """Parse a repeats file in the .json format

    Args:
        file_handle(iterable(str))

    Returns:
        repeat_info(dict)
    """
    repeat_info = {}
    try:
        raw_info = yaml.safe_load(file_handle)
    except yaml.YAMLError as err:
        raise SyntaxError("Repeats file is malformed")
    for i,repeat_unit in enumerate(raw_info, 1):
        try:
            repid = repeat_unit['LocusId']
        except KeyError as err:
            raise SyntaxError("Repeat number {0} is missing 'LocusId'".format(i))
        try:
            normal_max = repeat_unit['NormalMax']
        except KeyError as err:
            LOG.warning("Repeat number {0} ({1}) is missing 'NormalMax'. Skipping..".format(i,repid))
            continue
        try:
            pathologic_min = repeat_unit['PathologicMin']
        except KeyError as err:
            LOG.warning("Repeat number {0} ({1}) is missing 'PathologicMin'. Skipping..".format(i,repid))
            continue

        # ExHu 3.0 release candidate repids include the pathologic region of interest, but not the final version
        repeat_info[repid] = dict(normal_max=normal_max, pathologic_min=pathologic_min)

        for annotated_key in ANNOTATE_REPEAT_KEYS:
            if repeat_unit.get(annotated_key):
                repeat_info[repid][annotated_key] = repeat_unit.get(annotated_key)

        # From ExHu 3.0 repids include the region of interest.
        try:
            reference_region = repeat_unit['ReferenceRegion']
        except KeyError as err:
            LOG.warning("Repeat number {0} ({1}) is missing 'ReferenceRegion'. Skipping..".format(i,repid))
            continue
        if 'PathologicRegion' in repeat_unit:
            repid += "_" + repeat_unit['PathologicRegion']
        else:
            try:
                repid += "_" + reference_region
            except TypeError as err:
                LOG.warning("Repeat number {0} ({1}) has multiple 'ReferenceRegion' but no 'PathologicRegion'. Skipping..".format(i,repid))
                continue

        # ExHu 3.0 release candidate repids include the pathologic region of interest, but not the final version
        repeat_info[repid] = dict(normal_max=normal_max, pathologic_min=pathologic_min)

        for annotated_key in ANNOTATE_REPEAT_KEYS:
            if repeat_unit.get(annotated_key):
                repeat_info[repid][annotated_key] = repeat_unit.get(annotated_key)

    return repeat_info


def parse_repeat_file(file_handle, repeats_file_type='tsv'):
    """Parse a file with information about the repeats

    Args:
        file_handle(iterable(str))

    Returns:
        repeat_info(dict)
    """
    repeat_info = {}
    if repeats_file_type == 'tsv':
        repeat_info = parse_tsv(file_handle)
    elif repeats_file_type == 'json':
        repeat_info = parse_json(file_handle)

    return repeat_info

def get_repeat_info(variant_info, repeat_info):
    """Find the correct mutation level of a str variant

    Args:
        variant_line(str): A vcf variant line
        repeat_info(dict)

    Returns:
        (dict): With repeat level, lower and upper limits
    """
    repeat_strings = []
    # There can be one or two alternatives
    alleles = variant_info['alts']
    repeat_id = variant_info['info_dict'].get('REPID')
    if not repeat_id in repeat_info:
        LOG.warning("No info for repeat id %s", repeat_id)
        return None

    rep_lower = repeat_info[repeat_id].get('normal_max', -1)
    rep_upper = repeat_info[repeat_id].get('pathologic_min', -1)
    rank_score = 0
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
            if rank_score < RANK_SCORE['normal']:
                rank_score = RANK_SCORE['normal']
        elif repeat_number <= rep_upper:
            repeat_strings.append('pre_mutation')
            if rank_score < RANK_SCORE['pre_mutation']:
                rank_score = RANK_SCORE['pre_mutation']
        else:
            repeat_strings.append('full_mutation')
            rank_score = RANK_SCORE['full_mutation']

    repeat_data = dict(repeat_strings=','.join(repeat_strings), lower=rep_lower,
                upper=rep_upper, rank_score=rank_score)

    for annotate_repeat_key in ANNOTATE_REPEAT_KEYS:
        if repeat_info[repeat_id].get(annotate_repeat_key):
            repeat_data[annotate_repeat_key] = str(repeat_info[repeat_id][annotate_repeat_key])

    return repeat_data

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
        split_annotation = annotation.split('=')
        key = split_annotation[0]
        if len(split_annotation) == 1:
            info_dict[key] = None
            continue
        value = split_annotation[1]
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
