# Kaiju

> [Kaiju](http://kaiju.binf.ku.dk/) is a program for the taxonomic classification of high-throughput sequencing reads, e.g., Illumina or Roche/454, from whole-genome sequencing of metagenomic DNA. Reads are directly assigned to taxa using the NCBI taxonomy and a reference database of protein sequences from microbial and viral genomes.

## Profile Format

The following format is expected:

| Column Header | Description |
| ------------- | ----------- |
| file          |             |
| percent       |             |
| reads         |             |
| taxon_id      |             |
| taxon_name    |             |

## Example

```bash
file	percent	reads	taxon_id	taxon_name
barcode41_se-barcode41-kaiju.tsv	2.988734	841	28901	taxonid:28901
barcode41_se-barcode41-kaiju.tsv	2.739969	771	1902245	taxonid:1902245
barcode41_se-barcode41-kaiju.tsv	2.057642	579	2760310	taxonid:2760310
barcode41_se-barcode41-kaiju.tsv	1.929706	543	1108	taxonid:1108
```
