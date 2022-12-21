# DIAMOND

> [DIAMOND](https://github.com/bbuchfink/diamond) is a sequence aligner for protein and translated DNA searches, designed for high performance analysis of big sequence data.

## Profile Format

Taxpasta expects a tab-separated file with three columns. This is generated with the DIAMOND parameter `--outfmt 102`. Taxpasta will interpret the columns as:

| Column Header | Description |
|---------------|-------------|
| query_id      |             |
| taxonomy_id   |             |
| e_value       |             |
