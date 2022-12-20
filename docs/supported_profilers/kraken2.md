# Kraken2

> [Kraken2](https://ccb.jhu.edu/software/kraken2/) is a taxonomic classification system using exact k-mer matches to achieve high accuracy and fast classification speeds. This classifier matches each k-mer within a query sequence to the lowest common ancestor (LCA) of all genomes containing the given k-mer.

## Profile Format

A tab-separated output file with either six or eight columns as described [in the documentation](https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown#sample-report-output-format). Taxpasta interprets the columns as follows:

| Column Header         | Description |
|-----------------------|-------------|
| percent               |             |
| clade_assigned_reads  |             |
| direct_assigned_reads |             |
| num_minimizers        | optional    |
| distinct_minimizers   | optional    |
| taxonomy_lvl        |             |
| taxonomy_id           |             |
| name                  |             |
