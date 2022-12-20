# MALT

<!-- TODO: maybe we should rename these to use MEGAN as actually rma2info is from the MEGAN6 pacakge -->

> [MALT](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/malt/) performs alignment of metagenomic reads against a database of reference sequences (such as NR, GenBank or Silva) and produces a MEGAN RMA file as output.

An important thing to note is that `taxpasta` does not support the 'out of the box' formats provided by MALT (SAM, RMA6) as these are either not tabular or in non-open formats. Rather, `taxpasta` processes the output of the `rma2info` companion tool from the [MEGAN6 package](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/megan6/).

Therefore, if you wish to standardise MALT output you must run your RMA6 files through `rma2info` and supply the output of this tool as input to the `taxpasta` commands.

## Profile Format

Taxpasta expects a two-column, tab-separated file. It interprets the columns as:

| Column Header         | Description |
|-----------------------|-------------|
| taxonomy_id           |             |
| count                 |             |
