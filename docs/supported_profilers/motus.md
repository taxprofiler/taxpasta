# mOTUs

> The [mOTU](https://github.com/motu-tool/mOTUs/wiki) profiler is a computational tool that estimates relative taxonomic abundance of known and currently unknown microbial community members using metagenomic shotgun sequencing data.

## Profile Format

Taxpasta expects a three-column, tab-separated file. This file is generated with the mOTUs parameter `-o` . It interprets the columns as:

| Column Header      | Description |
|--------------------|-------------|
| consensus_taxonomy |             |
| ncbi_tax_id        |             |
| read_count *       |             |

> * Value used in standardised profile output 

## Example

```text
# git tag version 3.0.3 |  motus version 3.0.3 | map_tax 3.0.3 | gene database: nr3.0.3 | calc_mgc 3.0.3 -y insert.scaled_counts -l 75 | calc_motu 3.0.3 -k mOTU -C no_CAMI -g 3 -c -p | taxonomy: ref_mOTU_3.0.3 meta_mOTU_3.0.3
# call: python /usr/local/bin/../share/motus-3.0.1//motus profile -p -c -f ERX5474932_ERR5766176_1.fastq.gz -r ERX5474932_ERR5766176_2.fastq.gz -db db_mOTU -t 2 -n 2612_pe-ERR5766176-db_mOTU -o 2612_pe-ERR5766176-db_mOTU.out
#consensus_taxonomy	NCBI_tax_id	2612_pe-ERR5766176-db_mOTU
Leptospira alexanderi [ref_mOTU_v3_00001]	100053	0
Leptospira weilii [ref_mOTU_v3_00002]	28184	0
Chryseobacterium sp. [ref_mOTU_v3_00004]	NA	0
```