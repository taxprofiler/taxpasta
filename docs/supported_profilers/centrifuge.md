# Centrifuge

> [Centrifuge](https://ccb.jhu.edu/software/centrifuge/) is a very rapid and memory-efficient system for the classification of DNA sequences from microbial samples, with better sensitivity than and comparable accuracy to other leading systems. The system uses a novel indexing scheme based on the Burrows-Wheeler transform (BWT) and the Ferragina-Manzini (FM) index, optimized specifically for the metagenomic classification problem. Centrifuge requires a relatively small index (e.g., 4.3 GB for ~4,100 bacterial genomes) yet provides very fast classification speed, allowing it to process a typical DNA sequencing run within an hour.

## Profile Format

A `txt` output file produced by [`centrifuge-kreport`](https://ccb.jhu.edu/software/centrifuge/manual.shtml#kraken-style-report) is accepted by `taxpasta`.

| Column Header         | Description |
|-----------------------|-------------|
| percent               |             |
| clade_assigned_reads  |             |
| direct_assigned_reads |             |
| taxonomy_level        |             |
| taxonomy_id           |             |
| name                  |             |
