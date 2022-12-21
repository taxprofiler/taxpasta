# Kaiju

> [Kaiju](http://kaiju.binf.ku.dk/) is a program for the taxonomic classification of high-throughput sequencing reads, e.g., Illumina or Roche/454, from whole-genome sequencing of metagenomic DNA. Reads are directly assigned to taxa using the NCBI taxonomy and a reference database of protein sequences from microbial and viral genomes.

## Profile Format

Taxpasta expects a five column output.  This is generated either by redirecting the Kaiju `stdout` or the `-o` parameter. The following format is expected:

| Column Header | Description |
|---------------|-------------|
| file          |             |
| percent       |             |
| reads         |             |
| taxon_id      |             |
| taxon_name    |             |
