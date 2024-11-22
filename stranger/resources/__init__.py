try:
    from importlib.resources import files
except ImportError:
    # Try backported to piPY<37 `importlib_resources`.
    from importlib_resources import files

###### Files ######

# Repeat info files

repeats_file = "resources/repeatexpansionsloci.tsv"
repeats_json = "resources/variant_catalog_grch37.json"

###### Paths ######

# Backround data path

repeats_path = files("stranger").joinpath(repeats_file)
repeats_json_path = files("stranger").joinpath(repeats_json)
