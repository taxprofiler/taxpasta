# KMCP

> [KMCP](https://github.com/shenwei356/kmcp) uses genome coverage information by splitting the reference genomes into chunks and stores k-mers in a modified and optimized Compact Bit-Sliced Signature (COBS) index for fast alignment-free sequence searching. KMCP combines k-mer similarity and genome coverage information to reduce the false positive rate of k-mer-based taxonomic classification and profiling methods.

## Profile Format

Taxpasta expects a tab-separated file with seventeen columns. This is generated with the `kmcp profile` command. Taxpasta will interpret the columns as:

| Column Header     | Description |
| ----------------- | ----------- |
| ref               |             |
| percentage        |             |
| coverage          |             |
| score             |             |
| chunksFrac        |             |
| chunksRelDepth    |             |
| chunksRelDepthStd |             |
| reads             |             |
| ureads            |             |
| hicureads         |             |
| refsize           |             |
| refname           |             |
| taxid             |             |
| rank              |             |
| taxname           |             |
| taxpath           |             |
| taxpathsn         |             |

See [KMCP docs](https://bioinf.shenwei.me/kmcp/usage/#profile) for further description.
