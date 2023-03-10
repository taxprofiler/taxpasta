# Kraken2

> [Kraken2](https://ccb.jhu.edu/software/kraken2/) is a taxonomic classification system using exact k-mer matches to achieve high accuracy and fast classification speeds. This classifier matches each k-mer within a query sequence to the lowest common ancestor (LCA) of all genomes containing the given k-mer.

## Profile Format

A tab-separated kraken-report output file with either six or eight columns as described [in the documentation](https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown#sample-report-output-format). This is generated with the Kraken2 parameter `--report`. Taxpasta interprets the columns as follows:

| Column Header             | Description |
| ------------------------- | ----------- |
| percent                   |             |
| clade_assigned_reads      |             |
| direct_assigned_reads[^1] |             |
| num_minimizers            | optional    |
| distinct_minimizers       | optional    |
| taxonomy_lvl              |             |
| taxonomy_id               |             |
| name                      |             |

[^1]: Value used in standardised profile output

## Example

```text
 99.98	787758	787758	U	0	unclassified
  0.02	119	0	R	1	root
  0.02	119	0	R1	131567	  cellular organisms
  0.02	119	0	D	2759	    Eukaryota
  0.02	119	0	D1	33154	      Opisthokonta
  0.01	96	0	K	4751	        Fungi
  0.01	96	0	K1	451864	          Dikarya
```
