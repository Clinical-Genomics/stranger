# Stranger 
![Build Status - GitHub][actions-build-status]
[![PyPI Version][pypi-img]][pypi-url]
[![DOI][doi-image]][doi-url]
![GitHub Release Date][github-release-date]
[![Coverage Status][codecov-img]][codecov-url]
[![Code style: black][black-image]][black-url]
[![Woke][woke-image]][woke-url]

Annotates output files from [ExpansionHunter][hunter] and [TRGT][trgt] with the pathologic implications of the repeat sizes.

## Installation

Stranger uses the `uv` project manager. It is very quick and lightweight - see the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

```
git clone github.com/clinical-genomics/stranger
cd stranger
uv pip install --editable .
```

## Usage

```
uv run stranger --help
Usage: stranger [OPTIONS] VCF

  Annotate str variants with str status

Options:
  -f, --repeats-file PATH         Path to a file with repeat definitions. See
                                  README for explanation  [default: $HOME/
                                  stranger/stranger/resources/vari
                                  ant_catalog_grch37.json]
  -i, --family_id TEXT
  -t, --trgt                      File was produced with TRGT
  --version
  --loglevel [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set the level of log output.  [default:
                                  INFO]
  --help                          Show this message and exit.
```


## Repeat definitions

The repeats are called with Expansion Hunter as mentioned earlier. ExpansionHunter will annotate the number of times that a repeat has been seen in the bam files of each individual and what repeat id the variant has.
Stranger will annotate the level of pathogenicity for the repeat number. The intervals that comes with the package are manually collected from the literature since there is no single source where this information can be collected.

You can find a demo repeat definitions json file that comes with Stranger [here](https://github.com/Clinical-Genomics/stranger/blob/main/stranger/resources/variant_catalog_grch37.json). It is based on the ExpansionHunter variant catalog, but extended with a few disease locus relevant keys:
It is advisable to use an up to date file, perhaps based on a curated public repostitory such as [STRchive][strchive] or [STRipy][stripy]. The ones we use in our routine pipelines can be found at our [Reference-files repository][reference-files] and include our literature curation.

| Column/Key      | Content/Value                                                                                   |
|-----------------|-------------------------------------------------------------------------------------------------|
| HGNC_ID         | HGNC identifier for the repeat or most associated gene.                                         |
| HGNC_SYMBOL     | HGNC symbol for the repeat or most associated gene.                                             |
| REPID           | ExpansionHunter repeat ID.                                                                      |
| RU              | Basic repeat unit, as seen in ExpansionHunter. Unused.                                          |
| DisplayRU       | Repeat unit, as clinicians are used to see it.                                                  |
| Normal_Max      | (#copies) Longest repeat expected for normal individual; higher are marked pre- or full-mutation |
| Pathologic_Min  | (#copies) Shortest repeat expected for pathology. This and higher is annotated as full-mutation. |
| Disease         | Associated disease.                                                                             |
| InheritanceMode | Mode of inheritance "AR", "AD", "XR" etc                                                        |
| Source          | Reference literature resource type, eg GeneReviews or PubMed                                    |
| SourceId        | PMID or GeneReviews book ID for references                                                      |
| TRID            | Trgt repeat ID if not same as REPID                                                             |
| PathologicStruc | Array of index for pathogenic motif                                                             |


Other fields accepted by ExpansionHunter are also encouraged.

<details>
<summary>For convenience, here is a formatted table with some of the current contents.</summary>

| HGNCId | LocusId | DisplayRU | InheritanceMode | normal_max | pathologic_min | Disease | SourceDisplay | SourceId |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 3776 | AFF2 | CCG | XR | 39 | 200 | Fraxe | GeneReviews Internet 2019-11-07 | NBK535148 |
| 644 | AR | CAG | XR | 34 | 38 | SBMA | GeneReviews Internet 2019-11-07 | NBK535148 |
| 18060 | ARX_EIEE | GCN | XR | 16 | 17 | EIEE | GeneReviews Internet 2019-11-07 | NBK535148 |
| 18060 | ARX_PRTS | GCN | XR | 12 | 20 | PRTS | GeneReviews Internet 2019-11-07 | NBK535148 |
| 3033 | ATN1 | CAG | AD | 35 | 48 | DRPLA | GeneReviews Internet 2019-11-07 | NBK535148 |
| 10549 | ATXN10 | ATTCT | AD | 32 | 800 | SCA10 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 10548 | ATXN1 | CAG | AD | 35 | 45 | SCA1 | GeneReviews Internet SCA1 2017-06-22 | NBK1184 |
| 10555 | ATXN2 | CAG | AD | 31 | 37 | SCA2 | GeneReviews Internet SCA2 2019-02-14 | NBK1275 |
| 7106 | ATXN3 | CAG | AD | 44 | 60 | MJD | GeneReviews Internet 2019-11-07 | NBK535148 |
| 10560 | ATXN7 | CAG | AD | 19 | 36 | SCA7 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 10561 | ATXN8OS | CTG | AD | 50 | 80 | SCA8 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 28337 | C9ORF72 | GGCCCC | AD | 25 | 40 | FTDALS1 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 1388 | CACNA1A | CAG | AD | 18 | 20 | SCA6 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 1541 | CBL | CCG | AD | 79 | 100 | FRAX11B | Jones et al Nature 1995 | 7603564 |
| 1541 | BEAN1 | TGGAA | AD | 10 | 40 | SCA31 | Sato et al AJHG 2009 | 7603564 |
| 13164 | CNBP | CCTG | AD | 30 | 75 | DM2 | GeneReviews Internet 2020-03-19 | NBK1466 |
| 2482 | CSTB | CCCCGCCCCGCG | AR | 3 | 30 | EPM1 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 2482 | DAB1 | ATTTC | AD | 16 | 31 | SCA37 | GeneReviews Internet 2019-05-30 | NBK541729 |
| 29284 | DIP2B | CGG | AD | 24 | 270 | FRA12A | GeneReviews Internet 2019-11-07 | NBK535148 |
| 2933 | DMPK | CTG | AD | 34 | 50 | DM1 | GeneReviews Internet 2019-10-03 | NBK1165 |
| 18683 | EIF4A3 | TCGGCAGCGGCGCAGCGAGG | AR | 9 | 10 | RCPS | GeneReviews Internet 2019-11-07 | NBK535148 |
| 3775 | FMR1 | CGG | XR | 55 | 200 | FragileX | GeneReviews Internet 2019-11-07 | NBK535148 |
| 1092 | FOXL2 | GCN | AD | 14 | 15 | BPES | GeneReviews Internet 2019-11-07 | NBK535148 |
| 3951 | FXN | GAA | AR | 35 | 51 | FRDA | GeneReviews Internet 2019-11-07 | NBK535148 |
| 4331 | GLS | GCA | AR | 20 | 90 | GDPAG | van Kuilenburg et al (2019) NEJM 380:1433-1441 | 30970188 |
| 5102 | HOXA13_I | GCN | AD | 14 | 22 | HFGS | GeneReviews Internet 2019-08-08 | NBK1423 |
| 5102 | HOXA13_II | GCN | AD | 12 | 18 | HFGS | GeneReviews Internet 2019-08-08 | NBK1423 |
| 5102 | HOXA13_III | GCN | AD | 18 | 24 | HFGS | GeneReviews Internet 2019-08-08 | NBK1423 |
| 5136 | HOXD13 | GCN | AD | 15 | 22 | SDTY5 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 4851 | HTT | CAG | AD | 36 | 40 | Huntington | GeneReviews Internet 2020-06-11 | NBK1305 |
| 14203 | JPH3 | CTG | AD | 28 | 40 | HDL2 | GeneReviews Internet 2019-06-27 | NBK1529 |
| 31708 | LRP12 | CGN | AD | 45 | 90 | OPDM1 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 1226 | GIPC1 | GGC | AD | 32 | 73 | OPDM2 | Deng et al (2020) AJHG 106(6):793-804 | 32413282 |
| 17043 | NIPA1 | GCN | AD | 8 | 10000 | ALS - susceptibility to | Tazelaar et al (2019) Neurobiol Aging 74:234.e9-234.e15 | 30342764 |
| 15911 | NOP56 | GGCCTG | AD | 14 | 650 | SCA36 | GeneReviews Internet 2014-08-07 | NBK231880 |
| 53924 | NOTCH2NLC | CGG | AD | 38 | 66 | NIID | GeneReviews Internet 2019-11-07 | NBK535148 |
| 8565 | PABPN1 | GCN | AD | 10 | 12 | OPMD | GeneReviews Internet 2014-02-20 | NBK1126 |
| 9143 | PHOX2B | GCN | AD | 20 | 25 | CCHS | GeneReviews Internet 2014-01-30 | NBK1427 |
| 9305 | PPP2R2B | CAG | AD | 32 | 51 | SCA12 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 16854 | RAPGEF2 | TTTCA | AD | 1 | 10 | FAME7 | Ishiura et al (2018) Nature Genetics 50;581-90 | 29507423 |
| 9969 | RFC1 | AARRG | AR | 11 | 12 | CANVAS | Cortese et al 2019 Nat Gen PMID: 30926972 | 30926972 |
| 31750 | SAMD12 | TTTCA | AD | 1 | 10 | FAME1 | Ishiura et al (2018) Nature Genetics 50;581-90 | 29507423 |
| 10472 | RUNX2 | GCN | AD | 17 | 20 | CCD | GeneReviews Internet 2019-11-07 | NBK535148 |
| 11199 | SOX3 | GCN | XR | 15 | 22 | MRGH | GeneReviews Internet 2019-11-07 | NBK535148 |
| 11588 | TBP | CAN | AD | 40 | 49 | SCA17 | GeneReviews Internet 2019-09-12 | NBK1438 |
| 11592 | TBX1 | GCN | AD | 15 | 25 | TOF | GeneReviews Internet 2019-11-07 | NBK535148 |
| 11634 | TCF4 | CTG | AD | 39 | 100 | FECD3 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 11969 | TNRC6A | TTTCA | AD | 1 | 10 | FAME6 | Ishiura et al (2018) Nature Genetics 50;581-90 | 29507423 |
| 15516 | XYLT1 | GGC | AR | 20 | 70 | DBQD2 | LaCroix et al (2018) AJHG 104(1):35-44 | 30554721 |
| 12873 | ZIC2 | GCN | AD | 15 | 25 | HPE5 | GeneReviews Internet 2019-11-07 | NBK535148 |
| 12874 | ZIC3 | GCN | XR | 10 | 12 | VACTERLX | GeneReviews Internet 2019-11-07 | NBK535148 |
| 9179 | POLG | CTG | - | 15 | 10000 | - | Research only. Contact CMMS, KUH, regarding findings. | CMMS |
</details>

Stranger can also read a legacy `.tsv` format file, structured like a [Scout][scout] gene panel, with STR specific columns.
The column names and keys correspond, but if in any kind of doubt, please read the code or use the json version.

As a default the file that follows the distribution is used but the users can create their own file.
Header line(s) should be preceded with a `#`.

It is also possible to use an ExpansionHunter variant catalog json file with corresponding keys added. E.g.
```
[
    {
        "VariantType": "Repeat",
        "LocusId": "ATXN2",
        "LocusStructure": "(GCT)*",
        "ReferenceRegion": "chr12:112036753-112036822",
        "Disease": "SCA2",
        "NormalMax": 31,
        "PathologicMin": 39
    },
    {
        "VariantType": "Repeat",
        "LocusId": "PABPN1",
        "LocusStructure": "(GCG)*",
        "ReferenceRegion": "chr14:23790681-23790699",
        "Disease": "OPMD",
        "NormalMax": 6,
        "PathologicMin": 9
    }
]
```

Such files are also provided with the distribution. PRs with updates are much appreciated.

## Output

Output is by annotated VCF, with keys `STR_STATUS`, `NormalMax` and `PathologicMin`.

```
##INFO=<ID=STR_STATUS,Number=A,Type=String,Description="Repeat expansion status. Alternatives in [normal, pre_mutation, full_mutation]">
4       3076603 .       C       <STR17>,<STR18> .       PASS    END=3076660;REF=19;RL=57;RU=CAG;VARID=HTT;REPID=HTT;STR_STATUS=normal,normal
```

## TRGT mode
The flag `--trgt` will instruct Stranger to accept [TRGT][trgt] style VCFs. In particular, motif copy numbers are parsed from the `GT.MC` field and motifs 
listed in the `PathologicStruc` entry of the reference catalog:
```JSON
    {
        "VariantType": "Repeat",
        "LocusId": "RAPGEF2",
        "HGNCId": 16854,
        "InheritanceMode": "AD",
        "DisplayRU": "TTTCA",
        "SourceDisplay": "Ishiura et al (2018) Nature Genetics 50 581-90",
        "Source": "PubMed",
        "SourceId": "29507423",
        "LocusStructure": "(TTTTA)*(TTTCA)*(TTTTA)*",
        "ReferenceRegion": [
            "4:160263679-160263703",
            "4:160263704-160263708",
            "4:160263709-160263768"
        ],
        "VariantType": [
            "Repeat",
            "Repeat",
            "Repeat"
        ],
        "VariantId": [
            "RAPGEF2_TTTTA_5P",
            "RAPGEF2",
            "RAPGEF2_TTTTA_3P"
        ],
        "PathologicRegion": "4:160263704-160263708",
        "PathologicStruc": [1],
        "Disease": "FAME7",
        "NormalMax": 1,
        "PathologicMin": 10
    },
```
and 
```VCF
...
##FORMAT=<ID=MC,Number=.,Type=String,Description="Motif counts per allele">
...
4	160263680	.	TTTATTTTATTTTATTTTATTTTATATTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATTTTATT	.	0	.	TRID=FAME7_RAPGEF2;END=160263770;MOTIFS=TTTTA,TTTCA;STRUC=(TTTTA)n(TTTCA)n(TTTTA)n;STR_STATUS=full_mutation;STR_NORMAL_MAX=1;STR_PATHOLOGIC_MIN=10;RankScore=internal_id_3:30;HGNCId=16854;InheritanceMode=AD;DisplayRU=TTTCA;SourceDisplay=Ishiura et al (2018) Nature Genetics 50 581-90;Source=PubMed;SourceId=29507423;Disease=FAME7	GT:AL:ALLR:SD:MC:MS:AP:AM	0/0:91,91:85-98,91-91:21,20:18_0,18_0:0(0-89)_1(89-89)_0(89-89),0(0-89)_1(89-89)_0(89-89):0.956044,0.956044:.,.	0/0:91,91:85-98,91-91:21,20:18_0,18_0:0(0-89)_1(89-89)_0(89-89),0(0-89)_1(89-89)_0(89-89):0.956044,0.956044:.,.	0/0:91,91:85-98,91-91:21,20:18_0,18_0:0(0-89)_1(89-89)_0(89-89),0(0-89)_1(89-89)_0(89-89):0.956044,0.956044:.,.
...
```

[hunter]: https://github.com/Illumina/ExpansionHunter
[trgt]: https://github.com/PacificBiosciences/trgt
[reference-files]: https://github.com/Clinical-Genomics/reference-files/tree/master/rare-disease/disease_loci/ExpansionHunter-v5.0.0
[strchive]:http://strchive.org
[stripy]:https://stripy.org/database
[scout]:https://github.com/Clinical-Genomics/scout
[pypi-img]: https://img.shields.io/pypi/v/stranger.svg?style=flat-square
[pypi-url]: https://pypi.python.org/pypi/stranger/
[codecov-img]: https://codecov.io/gh/Clinical-Genomics/stranger/branch/main/graph/badge.svg
[codecov-url]: https://codecov.io/gh/Clinical-Genomics/stranger
[doi-image]: https://zenodo.org/badge/158848858.svg
[doi-url]: https://zenodo.org/badge/latestdoi/158848858
[github-release-date]: https://img.shields.io/github/release-date/Clinical-Genomics/scout
[codecov-img]: https://codecov.io/gh/Clinical-Genomics/stranger/branch/main/graph/badge.svg
[codecov-url]: https://codecov.io/gh/Clinical-Genomics/stranger
[actions-build-status]: https://github.com/Clinical-Genomics/stranger/actions/workflows/build_and_publish.yml/badge.svg
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[woke-image]: https://github.com/Clinical-Genomics/stranger/actions/workflows/woke.yml/badge.svg
[woke-url]: https://github.com/Clinical-Genomics/stranger/actions/workflows/woke.yml