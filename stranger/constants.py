RANK_SCORE = {"normal": 10, "pre_mutation": 20, "full_mutation": 30}

ANNOTATE_REPEAT_KEYS_EXHU = [
    "HGNCId",
    "InheritanceMode",
    "DisplayRU",
    "SourceDisplay",
    "Source",
    "SourceId",
    "SweGenMean",
    "SweGenStd",
    "Disease",
]

ANNOTATE_REPEAT_KEYS_TRGT = [
    "HGNCId",
    "InheritanceMode",
    "DisplayRU",
    "SourceDisplay",
    "Source",
    "SourceId",
    "Disease",
    "Struc",
    "PathologicStruc",
]

ANNOTATE_REPEAT_KEYS = list(set(ANNOTATE_REPEAT_KEYS_EXHU + ANNOTATE_REPEAT_KEYS_TRGT))
