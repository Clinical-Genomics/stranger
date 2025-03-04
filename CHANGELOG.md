# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [0.9.4]
### Fixed
- Bug with no ref on multi-allele FORMAT decompose

## [0.9.3]
### Fixed
- Switch build system to uv-hatchling
- Version from importlib metadata

## [0.9.2]
### Fixed
- Use codecov badge and fix scout link on README page
- Added a test for TRGT MCs set to `.`
- Added CLI test for TRGT file
- Codecov upload hidden artifact issue
- Incorrect multisample, multiallele FORMAT output
- Write unannotated entries (not in definition file) to output (reverted to pre-0.9 behaviour)

## [0.9.1]
### Added
- Added github action test and release workflows
### Fixed
- Docs for TRGT annotation
- Fallback setting allele size to 0 if MC is only set to "." and TRGT annotation requested

## [0.9.0]
- Add Docker image
- Parse TRGT VCFs - in particular, decompose and parse FORMAT.MC
- Bring in updated loci references from raredisese reference-files
- Fix processing TRGT VCFs with missing MC and TRIDs without underscore [#59](https://github.com/Clinical-Genomics/stranger/pull/59)
- Updates to pathogenic motifs for two loci: RFC1, RAPGEF2

## [0.8.1]
Fix DAB1 pathologic repeat unit name
Update POLG coords, quite a bit on hg38

## [0.8.0]
Off by one error on PathogenticMin output. All affected have at least been cautioned pre_mutation with proper size.
Added script to check HGNCId-symbol correspondence against genenames.org.
Added script to compare two variant_catalogs and warn on disagreeing field items.
Sync min/max between hg19, hg38 for ATN1, DMPK, FMR1 and TBP.Update BEAN1 documentation reference.
Update PABPN1 source tag.
Update GLS and RFC1 hg19 coordinates (zero based off by one).
Update NIPA1 locus definition updating hg19 to the current ExHu one.
Update ARX and SOX3 0-based off by one. Usually unproblematic, but gives ugly gap on REViewer alignments.
Update HTT PathogenicMin and NormalMax so already reduced penetrance are pathogenic - and mark intermediate pre_mutation.
Update pathologic region annotation on (mostly hg38 liftOver) loci affecting alternate region naming for ATXN7, ATXN8OS, FXN, HTT, CNBP, NOP56.
Update DAB1 repeat unit (revcomp) and off by one coordinates.

## [0.7.1]
Update rank score model.

## [0.7]
Add a family_id option and print to RankScore elements.

## [0.6.1]
Updated hg38/grch38 variant catalog.

## [0.6]
Add InheritanceMode, DisplayRU, Source and SweGen keys to variant catalog and annotate them out.
Update variant catalog to match ExHu v4.
Update variant catalog to tentatively include GeneReviews entries.

## [0.5.6]
Add a simple rank score.
Template adding references to variant_catalog.

## [0.5.5]
Add normal and pathologic limits for each variant to the VCF
Update variant catalog to match ExHu v3.1.2.

## [0.5.4]
Update Manifest to include json resource file.

## [0.5.3]
Allow both REPID naming systems.
Make json file default, and include as a resource in the PyPi distribution.
Update normal range for AFF2 and TBP.

## [0.5.2]
Fixed REPID naming back to match final ExHu v3.0.

## [0.5.1]
Added PyPi badge to README.md.
Added disease name for OPMD.

## [0.5]
Added pathogenicity boundaries for PHOX3B, TCF4, DIP2B.
Added POLG repeat on request.
Fix repid naming for ExpansionHunter v3 RC.
