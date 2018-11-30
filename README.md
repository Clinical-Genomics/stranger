# Stranger

Annotates output files from [ExpansionHunter][hunter] with the pathologic implications of the repeat sizes.

## Installation

```
git clone github.com/moonso/stranger
cd stranger
pip install --editable .
```

## Usage

```
stranger --help
Usage: stranger [OPTIONS] VCF

  Annotate str variants with str status

Options:
  -f, --repeats-file PATH         Path to a file with repeat definitions. See
                                  README for explanation  [default: /Users/man
                                  smagnusson/Projects/stranger/stranger/resour
                                  ces/repeatexpansionsloci.tsv]
  --version
  --loglevel [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set the level of log output.  [default:
                                  INFO]
  --help                          Show this message and exit.

```


## Repeat definitions

The repeats are called with Expansion Hunter as mentioned earlier. Expansion Hunter will annotate the number of times that a repeat has been seen in the bam files of each individual and what repeat id the variant has.
Stranger will annotate the level of pathogenecity for the repeat number. The intervals that comes with the package are manually collected from the literature since there is no source where this information can be collected.
There is a repeat definitions file that comes with Stranger in `stranger/resources/repeatexpansionsloci.tsv`. This is a tsv formated file on the following format:

| hgnc_id | hgnc_symbol | repid | ru | normal_max | pathologic_min | disease |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 10548 | ATXN1 | ATXN1 | CAG | 35 | 45 | SCA1 |
| 10555 | ATXN2 | ATXN2 | CAG | 31 | 39 | SCA2 |
| 7106 | ATXN3 | ATXN3 | CAG | 44 | 60 | SCA3 |
| 1388 | CACNA1A | CACNA1A | CAG | 18 | 20 | SCA6 |
| 10560 | ATXN7 | ATXN7 | CAG | 19 | 37 | SCA7 |
| 10561 | ATXN8OS | ATXN8OS | CAG | 50 | 80 | SCA8 |
| 10549 | ATXN10 | ATXN10 | ATTCT | 32 | 800 | SCA10 |
| 9305 | PPP2R2B | PPP2R2B | CAG | 35 | 49 | SCA12 |
| 11588 | TBP | TBP | CAG | 31 | 49 | SCA17 |
| 3951 | FXN | FXN | CAG | 35 | 51 | FRDA |
| 4851 | HTT | HTT | CCG | 36 | 37 | Huntington |
| 3775 | FMR1 | FMR1 | CGG | 65 | 200 | FragileX |
| 3776 | AFF2 | AFF2 | CCG | 25 | 200 | FRAXE |
| 13164 | CNBP | CNBP | CCTG | 30 | 75 | DM2 |
| 2933 | DMPK | DMPK | CAG | 37 | 50 | DM1 |
| 3033 | ATN1 | ATN1 | CAG | 34 | 49 | DRPLA |
| 15911 | NOP56 | NOP56 | GGCCTG | 14 | 650 | SCA36 |
| 28337 | C9ORF72 | C9ORF72 | GGCCCC | 25 | 40 | FTDALS1 |
| 8565 | PABPN1 | PABPN1 | GCG | 6 | 10 | OPMD |
| 2482 | CSTB | CSTB | CGCGGGGCGGGG | 3 | 30 | EPM1 |
| 1541 | CBL | CBL | CGG | 79 | 100 | FRAX11B |
| 14203 | JPH3 | JPH3 | CTG | 28 | 40 | HDL2 |
| 644 | AR | AR | CAG | 35 | 38 | SBMA |

As a default the file that follows the distribution is used but the users can create their own file.
Header line(s) should be preceded with a `#`. 


[hunter]: https://github.com/Illumina/ExpansionHunter