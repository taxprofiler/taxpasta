# ganon

> [ganon](https://pirovc.github.io/ganon/) is designed to index large sets of genomic reference sequences and to classify reads against them efficiently. The tool uses Interleaved Bloom Filters as indices based on k-mers/minimizers. It was mainly developed, but not limited, to the metagenomics classification problem: quickly assign sequence fragments to their closest reference among thousands of references. After classification, taxonomic abundance is estimated and reported.

## Profile Format

Taxpasta expects a tab-separated file with nine columns. This is generated with the `ganon report` command. Taxpasta will interpret the columns as:

| Column Header | Description |
| ------------- | ----------- |
| rank          |             |
| target        |             |
| lineage       |             |
| name          |             |
| nr_unique[^1] |             |
| nr_shared     |             |
| nr_children   |             |
| nr_cumulative |             |
| pc_cumulative |             |

[^1]: Value used in standardised profile output, representing unambiguous reads that match that reference (i.e., multi-match reads, nor with child reads). See [ganon docs](https://pirovc.github.io/ganon/outputfiles/) for further description.

## Example

```text
unclassified	-	-	unclassified	0	0	0	174530	27.61288
root	1	1	root	0	0	457530	457530	72.38712
superkingdom	2	1|2	Bacteria	0	0	447016	447016	69.95031
superkingdom	2157	1|2157	Archaea	0	0	10514	10514	2.43680
phylum	1224	1|2|1224	Pseudomonadota	0	0	189513	189513	22.08574
```
