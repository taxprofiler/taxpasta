# standardise

## What

The purpose of the `standardise` (aka `standardize`) command is to take the output of a single sample
from a single taxonomic profiler and convert it into a standard format that is
compatible with the output of other profilers standardised by taxpasta.

## When

You should use `taxpasta standardise` when you want to standardise a single
taxonomic profile or multiple profiles independently but do not want to merge
them in a single table, for example, you wish to store them separately.

See [`merge`](merge.md) if you wish to both standardise and merge in one step to
generate a single table containing all samples.

!!! warning

    You should only use this command if you are interested in raw 'counts'! The
    standardised output will remove profiler specific information, such as
    names, percentages, and lineage information.

## How

To use this command, you need a single output file from a single taxonomic
profiler, the name of the tool, and to specify an output file name:

```bash
taxpasta standardise --profiler kraken2 --output sample_standardised.tsv sample.kreport.txt
```

where `sample.kreport.txt` is a taxonomic profiling report file from kraken2.

This will produce a file called `sample_standardised.tsv` that contains the
taxpasta 'standard' two column structure described [below](#why).

!!! tip

    `taxpasta standardise` will automagically attempt to guess the output format
    based on the output file extension. You can alternatively explicitly define
    this with the `--output-format` flag. See `taxpasta standardise --help` for
    all supported formats.

## Why

Take, for example, the following kraken2 output file.

```text
 99.98	787758	787758	U	0	unclassified
  0.02	119	0	R	1	root
  0.02	119	0	R1	131567	  cellular organisms
  0.02	119	0	D	2759	    Eukaryota
  0.02	119	0	D1	33154	      Opisthokonta
  0.01	96	0	K	4751	        Fungi
  0.01	96	0	K1	451864	          Dikarya
```

This output format is specific to kraken2 and is unlikely to be comparable with
other tools, as they will record this information in different formats.
Furthermore, the indentation system to show taxonomic rank depth is not
particularly 'machine-readable'; making it difficult to load it into spreadsheet
tools or tabular formats preferred by languages such as
[R](https://www.r-project.org/).

A more common format in metagenomics is to have a first column with the taxon
name and a second column with the number of sequence 'hits' against that
particular taxon. Note that this format also encodes common information across
most tools, whereas kraken2 includes information that may not be reported by
other profilers, such as a column with the fraction against a taxon of all hits.

We have chosen to reduce all taxa to their respective identifiers. We chose zero as the
identifier for unclassified reads. Since there are many downstream processing and
analytics methods
that assume integer read counts, we only support such a count or pseudo count column.

| taxonomy_id |  count |
| :---------- | -----: |
| 0           | 787758 |
| 1           |    119 |
| 131567      |    119 |
| 2759        |    119 |
| 33154       |    119 |
| 4751        |     96 |
| 451864      |     96 |

Taxpasta supports fairly diverse output formats but at the very least there should be
a header indicating each column, the first (`taxonomy_id`) denoting
which taxonomy identifier has the counts in the second column (`count`).

!!! info

    This subcommand is used internally in the `merge` command prior to merging
    multiple profiles into one table.

!!! danger

    Taxpasta will assume that all taxonomic profiles to be processed are based
    on the same underlying taxonomy. That means, taxpasta will happily join taxa
    by their identifier even if they stem from different taxonomies.
