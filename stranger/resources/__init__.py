import pkg_resources

###### Files ######

# Repeat info files

repeats_file = 'resources/repeatexpansionsloci.tsv'
repeats_json = 'resources/variant_catalog_grch37.json'

###### Paths ######

# Backround data path

repeats_path = pkg_resources.resource_filename('stranger', repeats_file)
repeats_json_path = pkg_resources.resource_filename('stranger', repeats_json)
