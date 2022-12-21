# KrakenUniq

> [KrakenUniq](https://github.com/fbreitwieser/krakenuniq) is a novel metagenomics classifier that combines the fast k-mer-based classification of Kraken with an efficient algorithm for assessing the coverage of unique k-mers found in each species in a dataset.

## Profile Format

Taxpasta expects a 9 column table. This file is generated with the KrakenUniq parameter `--output`. The accepted format is:

| Column Header | Description |
|---------------|-------------|
| %             |             |
| reads         |             |
| taxReads      |             |
| kmers         |             |
| dup           |             |
| cov           |             |
| taxID         |             |
| rank          |             |
| taxName       |             |