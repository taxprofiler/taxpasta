# KrakenUniq

> [KrakenUniq](https://github.com/fbreitwieser/krakenuniq) is a novel metagenomics classifier that combines the fast k-mer-based classification of Kraken with an efficient algorithm for assessing the coverage of unique k-mers found in each species in a dataset.

## Profile Format

Taxpasta expects a 9 column table. This file is generated with the KrakenUniq parameter `--output`. The accepted format is:

| Column Header | Description |
| ------------- | ----------- |
| %             |             |
| reads         |             |
| taxReads      |             |
| kmers         |             |
| dup           |             |
| cov           |             |
| taxID         |             |
| rank          |             |
| taxName       |             |

## Example

```text
# KrakenUniq v1.0.0 DATE:2022-11-03T07:44:13Z DB:customdb/ DB_SIZE:358660 WD:/tmp/tmprujvrgk2/krakenuniq
# CL:perl /mnt/archgen/users/james_fellows_yates/bin/miniconda3/envs/mamba/envs/krakenuniq/bin/krakenuniq --db customdb/ --threads 8 --output test1.krakenuniq.classified.txt --report-file test1.krakenuniq.report.txt test_1.fastq.gz
%	reads	taxReads	kmers	dup	cov	taxID	rank	taxName
100	100	0	7556	1.3	0.1268	1	no rank	root
100	100	0	7556	1.3	0.1268	10239	superkingdom	  Viruses
100	100	0	7556	1.3	0.1268	2559587	clade	    Riboviria
100	100	0	7556	1.3	0.1268	2732396	kingdom	      Orthornavirae
100	100	0	7556	1.3	0.1268	2732408	phylum	        Pisuviricota
100	100	0	7556	1.3	0.1268	2732506	class	          Pisoniviricetes
100	100	0	7556	1.3	0.1268	76804	order	            Nidovirales
100	100	0	7556	1.3	0.1268	2499399	suborder	              Cornidovirineae
100	100	0	7556	1.3	0.1268	11118	family	                Coronaviridae
100	100	0	7556	1.3	0.1268	2501931	subfamily	                  Orthocoronavirinae
100	100	0	7556	1.3	0.1268	694002	genus	                    Betacoronavirus
100	100	0	7556	1.3	0.1268	2509511	subgenus	                      Sarbecovirus
100	100	0	7556	1.3	0.1268	694009	species	                        Severe acute respiratory syndrome-related coronavirus
100	100	100	7556	1.3	0.1268	2697049	no rank	                          Severe acute respiratory syndrome coronavirus 2
```
