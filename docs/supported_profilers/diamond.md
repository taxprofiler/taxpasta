# DIAMOND

> [DIAMOND](https://github.com/bbuchfink/diamond) is a sequence aligner for protein and translated DNA searches, designed for high performance analysis of big sequence data.

## Profile Format

Taxpasta expects a tab-separated file with three columns. Taxpasta will interpret the columns as:

| Column Header | Description |
| ------------- | ----------- |
| query_id      |             |
| taxonomy_id   |             |
| e_value       |             |

## Example

```text
shigella_dysenteriae_958/1	511145	2.46e-08
shigella_dysenteriae_1069/1	511145	2.37e-07
escherichia_coli_308/1	511145	1.55e-12
shigella_dysenteriae_1418/1	1310613	7.75e-10
escherichia_coli_962/1	1310613	7.02e-06
shigella_dysenteriae_520/1	1310613	5.46e-12
shigella_dysenteriae_242/1	1310613	2.91e-12
escherichia_coli_1146/1	1310613	2.61e-11
escherichia_coli_551/1	1310613	1.94e-14
shigella_dysenteriae_1094/1	1310613	1.74e-13
shigella_dysenteriae_999/1	0	0
```
