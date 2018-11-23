import pkg_resources

###### Files ######

# Repeat info files

repeats_file = 'resources/repeatexpansionsloci.tsv'

###### Paths ######

# Backround data path

repeats_path = pkg_resources.resource_filename('stranger', repeats_file)
