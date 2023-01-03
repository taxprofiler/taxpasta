# mOTUs

> The [mOTU](https://github.com/motu-tool/mOTUs/wiki) profiler is a computational tool that estimates relative taxonomic abundance of known and currently unknown microbial community members using metagenomic shotgun sequencing data.

## Profile Format

Taxpasta expects a three-column, tab-separated file. This file is generated with the mOTUs parameter `-o` . It interprets the columns as:

| Column Header      | Description |
|--------------------|-------------|
| consensus_taxonomy |             |
| ncbi_tax_id        |             |
| read_count         |             |
