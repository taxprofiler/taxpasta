# MEGAN6/MALT

> [MEGAN6](https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/megan6/) is a comprehensive toolbox for interactively analyzing microbiome data. All the interactive tools you need in one application.

> [MALT](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/malt/) performs alignment of metagenomic reads against a database of reference sequences (such as NR, GenBank or Silva) and produces a MEGAN RMA file as output.

Taxpasta supports the tabular file format generated by MEGAN6's `rma2info` utility. This utility converts RMA6 files created by both MEGAN6 itself and MALT.

Therefore, if you wish to standardise MEGAN6/MALT output, you must run your RMA6 files through `rma2info` and supply the output of this tool as input to the `taxpasta` commands.

## Profile Format

Taxpasta expects a two-column, tab-separated file. This is generated either by redirecting the rma2info `stdout` or the `--out` parameter. It interprets the columns as:

| Column Header         | Description |
|-----------------------|-------------|
| taxonomy_id           |             |
| count                 |             |