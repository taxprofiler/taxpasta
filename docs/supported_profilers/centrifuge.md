# Centrifuge

> [Centrifuge](https://ccb.jhu.edu/software/centrifuge/) is a very rapid and memory-efficient system for the classification of DNA sequences from microbial samples, with better sensitivity than and comparable accuracy to other leading systems. The system uses a novel indexing scheme based on the Burrows-Wheeler transform (BWT) and the Ferragina-Manzini (FM) index, optimized specifically for the metagenomic classification problem. Centrifuge requires a relatively small index (e.g., 4.3 GB for ~4,100 bacterial genomes) yet provides very fast classification speed, allowing it to process a typical DNA sequencing run within an hour.

## Profile Format

A Kraken-style `txt` output file produced by the [`centrifuge-kreport`](https://ccb.jhu.edu/software/centrifuge/manual.shtml#kraken-style-report) auxiliary tool (a part of the Centrifuge package) is accepted by `taxpasta`.

| Column Header             | Description |
| ------------------------- | ----------- |
| percent                   |             |
| clade_assigned_reads      |             |
| direct_assigned_reads[^1] |             |
| taxonomy_level            |             |
| taxonomy_id               |             |
| name                      |             |

[^1]: Value used in standardised profile output

## Example

```text
  0.00	0	0	U	0	unclassified
100.00	99	0	-	1	root
 98.99	98	0	D	10239	  Viruses
 33.33	33	0	F	687329	    Anelloviridae
 23.23	23	1	G	687331	      Alphatorquevirus
  1.01	1	1	S	687340	        Torque teno virus 1
  1.01	1	1	S	687342	        Torque teno virus 3
```
