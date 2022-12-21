# merge

## What

The purpose of the `merge` command is to standardise and immediately combine
multiple taxonomic profiles from the same tool but different samples. This produces a
standard 'taxon table' in either wide or long format.

## How

To use this command, you will need multiple profiles of a single tool, the name
of the tool, and specify an output file name:

```bash
taxpasta merge --profiler kraken2 --output taxon_table.tsv sample1.kreport.txt sample2.kreport.txt sample3.kreport.txt
```

where `sample1.kreport.txt`, `sample2.kreport.txt`, `sample3.kreport.txt` are
report files from kraken2.

This will produce a file called `sample_standardised.tsv` that contains the
taxpasta 'standard' multi-column structure described [below](#why).

## When

You should use `taxpasta merge` when you want to standardise multiple profiles
in one go and have all profiles combined into a single table. You will
use this command if you want to load the table directly into a spreadsheet
program or programming language without needing to manually combine profiles.

See [`standardise`](standardise.md) if you wish to only standardise without merging.

!!! warning

    You should only use this command if you are interested in raw 'counts'! The
    standardised output will remove profiler specific information, such as
    names, percentages, and lineage information.

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
name and each subsequent column representing a different sample. Each cell
represents a count of the number of sequence hits against that row's taxon within
that column's sample.

We have chosen to reduce all taxa to their respective identifiers. We chose zero as the
identifier for unclassified reads. Since there are many downstream processing and
analytics methods
that assume integer read counts, we only support such a count or pseudo count column.

An example of this format could be:

| taxonomy_id | sample1 | sample2 | sample3 |
| :---------- | ------: | ------: | ------: |
| 0           |  787758 | 2233938 |   98872 |
| 1           |     119 |   12929 |     872 |
| 131567      |     119 |    5345 |     800 |
| 2759        |     119 |     123 |     200 |
| 33154       |     119 |     123 |      29 |
| 4751        |      96 |      30 |      29 |
| 451864      |      96 |      30 |      29 |

Where you have a header indicating each column, the first (`taxonomy_id`) indicating
which taxon has the counts in the second column (`sample1`), then third column
(`sample2`), fourth column (`sample3`), and so on.

As you can see here, this is a much more compact way of looking at multiple
samples, with the caveat that you may not have additional information, such as the
accuracy of each assignment.

!!! danger

    Taxpasta will assume that all taxonomic profiles to be processed are based
    on the same underlying taxonomy. That means, taxpasta will happily join taxa
    by their identifier even if they stem from different taxonomies.
