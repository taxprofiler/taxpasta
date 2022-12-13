# standardize

## What

The purpose of the `standarise` command is to take an output of a single taxonomic profiling tool, and convert it into a standard format that is compatible with the (also standardised) output of other profiling tools.

## How

To use this command, you need a single output file from a single taxonomic profiling tool, the name of the tool, and to specify an output file name:

```bash
taxpasta standardise --profiler kraken2 --output sample_standardised.tsv sample.kreport.txt
```

where `sample.kreport.txt` is a taxonomic profiling report file from Kraken2.

This will produce a file called `sample_standardised.tsv` that contains the taxpasta 'standard' two column structure described [below](#why).

> 💡 `taxpasta standardise` will automagically attempt to guess the output format based on the output file extension. You can alternatively explicitly define this with the `--output-format` flag. See `taxpasta standardise --help` for all supported formats.

## When

You should use `taxpasta standardise` when you want to standardise profiles of a single or multiple profiles independetly, but do not want to join them in a single table (e.g., if you wish to store them separately, and merge on the fly in your own script).

See [`merge`](merge.md) if you wish to both standardise and merge in one step to generate a single table containing all samples.

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

A more common format in metagenomics is to have a first column with the taxon name, and a second column with the number of sequence 'hits' against that particular taxon. Note that this format also encodes common information across most tools, whereas Kraken2 inclueds information that may not be reported by other tools (such as a column with the fraction against a taxon of all hits).

For an example a more common format of the above would be:

| taxon  | count  |
| ------ | ------ |
| 0      | 787758 |
| 1      | 119    |
| 131567 | 119    |
| 2759   | 119    |
| 33154  | 119    |
| 4751   | 96     |
| 451864 | 96     |

Where you have a header indicating each column, the first (`taxon`) indicating which taxon has the counts in the second column (`counts`)

> 🛈 This subcommand is used internally in the `merge` command prior to merging multiple profiles into one table.
