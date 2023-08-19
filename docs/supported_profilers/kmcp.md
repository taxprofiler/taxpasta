# KMCP

> [KMCP](https://github.com/shenwei356/kmcp) uses genome coverage information by splitting the reference genomes into chunks and stores k-mers in a modified and optimized Compact Bit-Sliced Signature (COBS) index for fast alignment-free sequence searching. KMCP combines k-mer similarity and genome coverage information to reduce the false positive rate of k-mer-based taxonomic classification and profiling methods.

## Profile Format

Taxpasta expects a tab-separated file with seventeen columns. This is generated with the `kmcp profile` command. Taxpasta will interpret the columns as:

| Column Header     | Description |
| ----------------- | ----------- |
| ref               |             |
| percentage        |             |
| coverage          | optional    |
| score             |             |
| chunksFrac        |             |
| chunksRelDepth    |             |
| chunksRelDepthStd | optional    |
| reads             |             |
| ureads            |             |
| hicureads         |             |
| refsize           |             |
| refname           | optional    |
| taxid             |             |
| rank              | optional    |
| taxname           | optional    |
| taxpath           | optional    |
| taxpathsn         | optional    |

Please refer to the [KMCP documentation](https://bioinf.shenwei.me/kmcp/usage/#profile) for further description.
