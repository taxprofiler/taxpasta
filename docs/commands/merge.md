# merge

## What

The purpose of the `merge` command is to standardise and immediately combine multiple taxonomic profiles of a given tool. This produces a standard 'taxon table' in either wide or long formats.

## How

To use this command, you will need multiple profiles of a single tool, the name of the tool, and specify an output file name.

```bash
taxpasta merge --profiler kraken2 --output taxon_table.tsv sample1.kreport.txt sample2.kreport.txt sample3.kreport.txt
```

where `sample1.kreport.txt`, `sample2.kreport.txt`, `sample3.kreport.txt` are taxonomic profiling report files from Kraken2.

This will produce a file called `sample_standardised.tsv` that contains the taxpasta 'standard' multi-column structure described [below](#why).

## When

You should use `taxpasta merge` when you want to standardise profiles multiple profiles in one go, and have all profiles combined into a single table. You will use this command if you want to load the table directly into a spreadsheet program or programming langauge without needing to manually combine profiles.

See [`standardise`](standardise.md) if wish to only standardise without merging.

> ⚠️ You should only use this command if you are interested in raw 'counts'! The output will remove other information that maybe stored in the tool (percentages, lineage information etc.,)

## Why

For example, take the following Kraken2 output file.

```text
 99.98	787758	787758	U	0	unclassified
  0.02	119	0	R	1	root
  0.02	119	0	R1	131567	  cellular organisms
  0.02	119	0	D	2759	    Eukaryota
  0.02	119	0	D1	33154	      Opisthokonta
  0.01	96	0	K	4751	        Fungi
  0.01	96	0	K1	451864	          Dikarya
```

This output format is specific to Kraken2, and is unlikely to be comparable to other tools, as they will record this information in different formats. Furthermore, the indentation system to show taxonomic rank depth is not particularly 'machine-readable', making it difficult to load into spreadsheet tools or tabular formats preferred by languages such as R.

As there is multiple bits of information of just this sample (percentage, rank etc.), this format makes it very difficult to rapidly compare between different samples.

A more common format in metagenomics is to have a first column with the taxon name, and each subsequent column representing a different sample with each cell having a count of the number of sequence hits against each species (rows) from each sample (columns).

For example, a more common format of the above would be:

| taxon  | sample1 | sample2 | sample3 |
| ------ | ------- | ------- | ------- |
| 0      | 787758  | 2233938 | 98872   |
| 1      | 119     | 12929   | 872     |
| 131567 | 119     | 5345    | 800     |
| 2759   | 119     | 123     | 200     |
| 33154  | 119     | 123     | 29      |
| 4751   | 96      | 30      | 29      |
| 451864 | 96      | 30      | 29      |

Where you have a header indicating each column, the first (`taxon`) indicating which taxon has the counts in the second column (`sample1`), then third column (`sample2`), fourth column (`sample3`), and so on.

As you can see here, this is a much more compact way of viewing across multiple samples, with the caveat you may not have additional information about the accuracy of each assignment (such as edit distances, sub-kmers etc.).
