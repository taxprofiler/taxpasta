# Bracken

Bracken (Bayesian Reestimation of Abundance with KrakEN) is a highly accurate statistical method that computes the abundance of species in DNA sequences from a metagenomics sample. Braken uses the taxonomy labels assigned by Kraken, a highly accurate metagenomics classification algorithm, to estimate the number of reads originating from each species present in a sample.

The following format is accepted by `taxpasta`:

| name | taxonomy_id | taxonomy_lvl | kraken_assigned_reads | added_reads | new_est_reads | fraction_total_reads |
