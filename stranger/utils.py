import copy
import logging
import re

import yaml

from stranger.constants import ANNOTATE_REPEAT_KEYS, RANK_SCORE

NUM = re.compile(r"\d+")

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
    for i, line in enumerate(file_handle, 1):
        if not len(line) > 1:
            continue
        line = line.rstrip()
        if line.startswith("#"):
            if not line.startswith("##"):
                header = line[1:].split("\t")
            continue
        line = line.split("\t")
        if not len(line) == len(header):
            LOG.warning("\t".join(line))
            raise SyntaxError("Line {0} is malformed".format(i))
        repeat = dict(zip(header, line))
        try:
            repeat["hgnc_id"] = int(repeat["hgnc_id"])
            repeat["normal_max"] = int(repeat["normal_max"])
            repeat["pathologic_min"] = int(repeat["pathologic_min"])
        except ValueError as err:
            LOG.warning("Line %s is malformed", i)
            LOG.warning("\t".join(line))
            raise err
        repeat_info[repeat["repid"]] = repeat

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
    for i, repeat_unit in enumerate(raw_info, 1):
        try:
            repid = repeat_unit["LocusId"]
        except KeyError as err:
            raise SyntaxError("Repeat number {0} is missing 'LocusId'".format(i))
        try:
            normal_max = repeat_unit["NormalMax"]
        except KeyError as err:
            LOG.warning(
                "Repeat number {0} ({1}) is missing 'NormalMax'. Skipping..".format(i, repid)
            )
            continue
        try:
            pathologic_min = repeat_unit["PathologicMin"]
        except KeyError as err:
            LOG.warning(
                "Repeat number {0} ({1}) is missing 'PathologicMin'. Skipping..".format(i, repid)
            )
            continue

        # ExHu 3.0 release candidate repids include the pathologic region of interest, but not the final version
        repeat_info[repid] = dict(normal_max=normal_max, pathologic_min=pathologic_min)

        for annotated_key in ANNOTATE_REPEAT_KEYS:
            if repeat_unit.get(annotated_key):
                repeat_info[repid][annotated_key] = repeat_unit.get(annotated_key)

        if "PathologicStruc" in repeat_unit:
            repeat_info[repid]["pathologic_struc"] = repeat_unit["PathologicStruc"]

        if "TRID" in repeat_unit:
            # TRGT uses TRID instead of REPID
            trid = repeat_unit["TRID"]

            repeat_info[trid] = dict(normal_max=normal_max, pathologic_min=pathologic_min)

            for annotated_key in ANNOTATE_REPEAT_KEYS:
                if repeat_unit.get(annotated_key):
                    repeat_info[trid][annotated_key] = repeat_unit.get(annotated_key)

            if "PathologicStruc" in repeat_unit:
                repeat_info[trid]["pathologic_struc"] = repeat_unit["PathologicStruc"]

        # From ExHu 3.0 repids include the region of interest.
        try:
            reference_region = repeat_unit["ReferenceRegion"]
        except KeyError as err:
            LOG.warning(
                "Repeat number {0} ({1}) is missing 'ReferenceRegion'. Skipping..".format(i, repid)
            )
            continue
        if "PathologicRegion" in repeat_unit:
            repid += "_" + repeat_unit["PathologicRegion"]
        else:
            try:
                repid += "_" + reference_region
            except TypeError as err:
                LOG.warning(
                    "Repeat number {0} ({1}) has multiple 'ReferenceRegion' but no 'PathologicRegion'. Skipping..".format(
                        i, repid
                    )
                )
                continue

        # ExHu 3.0 release candidate repids include the pathologic region of interest, but not the final version
        repeat_info[repid] = dict(normal_max=normal_max, pathologic_min=pathologic_min)

        for annotated_key in ANNOTATE_REPEAT_KEYS:
            if repeat_unit.get(annotated_key):
                repeat_info[repid][annotated_key] = repeat_unit.get(annotated_key)

        if "PathologicStruc" in repeat_unit:
            repeat_info[repid]["pathologic_struc"] = repeat_unit["PathologicStruc"]

    return repeat_info


def parse_repeat_file(file_handle, repeats_file_type="tsv"):
    """Parse a file with information about the repeats

    Args:
        file_handle(iterable(str))

    Returns:
        repeat_info(dict)
    """
    repeat_info = {}
    if repeats_file_type == "tsv":
        repeat_info = parse_tsv(file_handle)
    elif repeats_file_type == "json":
        repeat_info = parse_json(file_handle)

    return repeat_info


def get_exhu_repeat_res_from_alts(variant_info: dict):
    alleles = variant_info["alts"]
    repeat_res = []
    for allele in alleles:
        if allele == ".":
            repeat_res.extend([0])
        else:
            repeat_res.extend([int(num) for num in NUM.findall(allele)])
        if not repeat_res:
            LOG.warning("Allele information is not on correct format: %s", allele)
            raise SyntaxError("Allele on wrong format")
    return repeat_res


def get_repeat_id(variant_info):
    """
    First tries to get variant id from REPID,
    if that is not sucessful, try to get variant id from TRID (TRGT).
    If the ID is formatted with underscore (STRchive),
    grab the part which is after the underscore, otherwise take the whole ID (PacBio).
    """
    info_dict = variant_info.get("info_dict", {})

    repid = info_dict.get("REPID")
    trid = info_dict.get("TRID")

    if repid:
        return repid

    if not trid:
        return None

    if "_" in trid:
        return trid.split("_", 1)[1]

    return trid


def get_repeat_info(variant_info: dict, repeat_info: dict) -> dict:
    """Find the correct mutation level of a str variant

    Args:
        variant_info(dict): A variant info dict (from VCF)
        repeat_info(dict): A repeat info dict (from config catalog)

    Returns:
        (dict): With repeat level, lower and upper limits
    """

    # There can be one or more alternatives (each ind can have at most two of those)
    repeat_id = get_repeat_id(variant_info)

    if not repeat_id in repeat_info:
        LOG.warning("No info for repeat id %s", repeat_id)
        return None

    rep_lower = repeat_info[repeat_id].get("normal_max", -1)
    rep_upper = repeat_info[repeat_id].get("pathologic_min", -1)
    rank_score = 0

    repeat_string = ""
    repeat_strings = []

    if variant_info.get("format_dicts"):
        repeat_res = get_trgt_repeat_res(variant_info, repeat_info)
    else:
        repeat_res = get_exhu_repeat_res_from_alts(variant_info)

    for repeat_number in repeat_res:
        if repeat_number <= rep_lower:
            repeat_strings.append("normal")
            if rank_score < RANK_SCORE["normal"]:
                rank_score = RANK_SCORE["normal"]
                repeat_string = "normal"
        elif repeat_number < rep_upper:
            repeat_strings.append("pre_mutation")
            if rank_score < RANK_SCORE["pre_mutation"]:
                rank_score = RANK_SCORE["pre_mutation"]
                repeat_string = "pre_mutation"
        else:
            repeat_strings.append("full_mutation")
            rank_score = RANK_SCORE["full_mutation"]
            repeat_string = "full_mutation"

    repeat_data = dict(
        most_severe_repeat_string=repeat_string,
        repeat_strings=repeat_strings,
        lower=rep_lower,
        upper=rep_upper,
        rank_score=rank_score,
    )

    for annotate_repeat_key in ANNOTATE_REPEAT_KEYS:
        if repeat_info[repeat_id].get(annotate_repeat_key):
            repeat_data[annotate_repeat_key] = str(repeat_info[repeat_id][annotate_repeat_key])

    return repeat_data


def get_trgt_repeat_res(variant_info, repeat_info):
    """Convert target variant info into ExHu count format, splitting entries if needed,
    if they turn out to contain more than one allele or more than one motif.

    The repeat definitions may have information on which motifs are to be counted towards pathogenicity.
    If no such PATHOLOGIC_STRUC info is available, default to use all motif parts.
    """

    repeat_id = get_repeat_id(variant_info)

    if not repeat_id in repeat_info:
        LOG.warning("No info for repeat id %s", repeat_id)
        return None

    repeat_res = []
    for format_dict in variant_info["format_dicts"]:
        pathologic_counts = 0
        mc = format_dict.get("MC")
        if mc:
            for allele in mc.split(","):
                mcs = allele.split("_")
                # GT would have the index of the MC in the ALT field list if we wanted to be specific...

                # What should we do if MC is . ?
                if allele == ".":
                    repeat_res.extend([0])
                    continue

                if len(mcs) > 1:
                    pathologic_mcs = repeat_info[repeat_id].get("pathologic_struc", range(len(mcs)))

                    for index, count in enumerate(mcs):
                        if index in pathologic_mcs:
                            pathologic_counts += int(count)
                else:
                    pathologic_counts = int(allele)
        repeat_res.append(pathologic_counts)

    return repeat_res


def get_info_dict(info_string):
    """Convert an info string to a dictionary

    Args:
        info_string(str): A string that contains the INFO field from a vcf variant

    Returns:
        info_dict(dict): The input converted to a dictionary
    """
    info_dict = {}
    if not info_string:
        return info_dict
    if info_string == ".":
        return info_dict

    for annotation in info_string.split(";"):
        split_annotation = annotation.split("=")
        key = split_annotation[0]
        if len(split_annotation) == 1:
            info_dict[key] = None
            continue
        value = split_annotation[1]
        info_dict[key] = value

    return info_dict


def get_format_dicts(format_string: str, format_sample_strings: list) -> list:
    """
    Convert format declaration string and list of sample format strings into a
    list of format dicts, one dict per individual
    """
    if not format_string:
        return None

    format_fields = format_string.split(":")

    format_dicts = [
        dict(zip(format_fields, individual_format.split(":")))
        for index, individual_format in enumerate(format_sample_strings)
    ]

    return format_dicts


def get_variant_line(variant_info, header_info):
    """Convert variant dictionary back to a VCF formated string

    Args:
        variant_info(dict):
        header_info(list)

    Returns:
        variant_string(str): VCF formatted variant
    """

    info_dict = variant_info["info_dict"]
    if not info_dict:
        variant_info["INFO"] = "."
    else:
        info_list = []
        for annotation in info_dict:
            if info_dict[annotation] is None:
                info_list.append(annotation)
                continue
            info_list.append("=".join([annotation, info_dict[annotation]]))
        variant_info["INFO"] = ";".join(info_list)

    variant_list = []
    for annotation in header_info:
        variant_list.append(variant_info[annotation])

    return "\t".join(variant_list)


def get_individual_index(header_info):
    """Return index for first individual (FORMAT formatted) column in VCF"""

    for index, item in enumerate(header_info):
        if item.startswith("FORMAT"):
            individual_index = index + 1
    return individual_index


def update_decomposed_variant_format_fields(variant_info, header_info, individual_index):
    """
    Update variant_info individual FORMAT fields with information found in the now up to date
    format_dicts.
    """

    individuals = [individual for individual in header_info[individual_index:]]

    for index, format_dict in enumerate(variant_info["format_dicts"]):
        out_format = []
        for field in variant_info["FORMAT"].split(":"):
            out_format.append(format_dict[field])

        variant_info[individuals[index]] = ":".join(out_format)


def decompose_var(variant_info):
    """
    Decompose variant with more than one alt into multiple ones, with mostly the same info except on GT and ALT.

    Make new resulting variant info lines, copied from original but with decomposable fields replaced appropriately.

    The index of the alt is also the number (-1) at the corresponding position in the GT field. Note 0-base in GT for
    reference.

    Individuals sharing none of the alleles on the newly decomposed row receive a "./." and "." for the FORMAT component.
    Corresponding split FORMAT values (except GT) get a "." for the ref component and for unclear/uncalled components.
    """

    result_variants = []
    for index, alt in enumerate(variant_info["alts"]):
        result_variants.append(copy.deepcopy(variant_info))
        result_variants[index]["ALT"] = variant_info["alts"][index]

    for index, alt in enumerate(variant_info["alts"]):

        for individual_index, format_dict in enumerate(variant_info["format_dicts"]):
            gts = format_dict["GT"].split("/")
            variant_component = None

            updated_fields = []
            for gt_component, decomposed_field in enumerate(gts):
                if decomposed_field in ["0", "."]:
                    # reference component 0, uncalled component .
                    updated_fields.append(decomposed_field)

                if decomposed_field.isdigit():
                    if int(decomposed_field) == index + 1:
                        # this is the variant component
                        variant_component = gt_component
                        updated_fields.append("1")
                    else:
                        # unclear component
                        updated_fields.append(".")

            result_variants[index]["format_dicts"][individual_index]["GT"] = "/".join(
                updated_fields
            )

            for field, individual_value in format_dict.items():
                if field in ["GT"]:
                    continue

                variant_component_value = (
                    individual_value.split(",")[variant_component]
                    if variant_component is not None
                    else "."
                )

                result_variants[index]["format_dicts"][individual_index][
                    field
                ] = variant_component_value

    return result_variants
