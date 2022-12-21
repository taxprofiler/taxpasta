# Bracken

> [Bracken](https://ccb.jhu.edu/software/bracken/) (Bayesian Reestimation of Abundance with KrakEN) is a highly accurate statistical method that computes the abundance of species in DNA sequences from a metagenomics sample. Bracken uses the taxonomy labels assigned by Kraken, a highly accurate metagenomics classification algorithm, to estimate the number of reads originating from each species present in a sample.

## Profile Format

The following input format is accepted by `taxpasta`. This file is generated with the Bracken parameter `-o`. A tab-separated file with the following column headers:

| Column Header         | Description |
|-----------------------|-------------|
| name                  |             |
| taxonomy_id           |             |
| taxonomy_lvl          |             |
| kraken_assigned_reads |             |
| added_reads           |             |
| new_est_reads         |             |
| fraction_total_reads  |             |
