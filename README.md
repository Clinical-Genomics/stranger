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





[hunter]: https://github.com/Illumina/ExpansionHunter