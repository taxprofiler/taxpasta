<!-- --8<-- [start:data-setup] -->

```bash
mkdir taxpasta-tutorial
cd taxpasta-tutorial
```

<!-- --8<-- [end:data-setup] -->
<!-- --8<-- [start:data-curl] -->

```bash
## mOTUs
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

## Kraken2
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt
```

<!-- --8<-- [end:data-curl] -->
<!-- --8<-- [start:data-wget] -->

```bash
## mOTUs
wget https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out
wget https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

## Kraken2
wget https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt
```

<!-- --8<-- [end:data-wget] -->
<!-- --8<-- [start:data-ls] -->

```bash
ls
```

    2612_pe-ERR5766176-db1.kraken2.report.txt  2612_se-ERR5766180-db_mOTU.out
    2612_pe-ERR5766176-db_mOTU.out

<!-- --8<-- [end:data-ls] -->
<!-- --8<-- [start:motus-head] -->

```bash
head 2612_pe-ERR5766176-db_mOTU.out
```

    # git tag version 3.0.3 |  motus version 3.0.3 | map_tax 3.0.3 | gene database: nr3.0.3 | calc_mgc 3.0.3 -y insert.scaled_counts -l 75 | calc_motu 3.0.3 -k mOTU -C no_CAMI -g 3 -c -p | taxonomy: ref_mOTU_3.0.3 meta_mOTU_3.0.3
    # call: python /usr/local/bin/../share/motus-3.0.1//motus profile -p -c -f ERX5474932_ERR5766176_1.fastq.gz -r ERX5474932_ERR5766176_2.fastq.gz -db db_mOTU -t 2 -n 2612_pe-ERR5766176-db_mOTU -o 2612_pe-ERR5766176-db_mOTU.out
    #consensus_taxonomy NCBI_tax_id 2612_pe-ERR5766176-db_mOTU
    Leptospira alexanderi [ref_mOTU_v3_00001]   100053  0
    Leptospira weilii [ref_mOTU_v3_00002]   28184   0
    Chryseobacterium sp. [ref_mOTU_v3_00004]    NA  0
    Chryseobacterium gallinarum [ref_mOTU_v3_00005] 1324352 0
    Chryseobacterium indologenes [ref_mOTU_v3_00006]    253 0
    Chryseobacterium artocarpi/ureilyticum [ref_mOTU_v3_00007]  NA  0
    Chryseobacterium jejuense [ref_mOTU_v3_00008]   445960  0

<!-- --8<-- [end:motus-head] -->
<!-- --8<-- [start:kraken2-head] -->

```bash
head 2612_pe-ERR5766176-db1.kraken2.report.txt
```

     99.97  627680  627680  U   0   unclassified
      0.03  168 0   R   1   root
      0.03  168 0   R1  131567    cellular organisms
      0.03  168 0   D   2759        Eukaryota
      0.03  168 0   D1  33154         Opisthokonta
      0.02  152 0   K   33208           Metazoa
      0.02  152 0   K1  6072              Eumetazoa
      0.02  152 0   K2  33213               Bilateria
      0.02  152 0   K3  33511                 Deuterostomia
      0.02  152 0   P   7711                    Chordata

<!-- --8<-- [end:kraken2-head] -->
<!-- --8<-- [start:standardise] -->

```bash
taxpasta standardise -p kraken2 -o 2612_pe-ERR5766176-db1_kraken2.tsv 2612_pe-ERR5766176-db1.kraken2.report.txt
```

    [INFO] Write result to '2612_pe-ERR5766176-db1_kraken2.tsv'.

<!-- --8<-- [end:standardise] -->
<!-- --8<-- [start:standardise-head] -->

```bash
head 2612_pe-ERR5766176-db1_kraken2.tsv
```

    taxonomy_id count
    0   627680
    1   0
    131567  0
    2759    0
    33154   0
    33208   0
    6072    0
    33213   0
    33511   0

<!-- --8<-- [end:standardise-head] -->
<!-- --8<-- [start:merge] -->

```bash
taxpasta merge -p motus -o dbMOTUs_motus.tsv 2612_pe-ERR5766176-db_mOTU.out 2612_se-ERR5766180-db_mOTU.out
```

    [WARNING] The merged profiles contained different taxa. Additional zeroes were introduced for missing taxa.
    [INFO] Write result to 'dbMOTUs_motus.tsv'.

<!-- --8<-- [end:merge] -->
<!-- --8<-- [start:merge-head] -->

```bash
head dbMOTUs_motus.tsv
```

    taxonomy_id 2612_pe-ERR5766176-db_mOTU  2612_se-ERR5766180-db_mOTU
    40518   20  2
    216816  1   0
    1680    6   1
    1262820 1   0
    74426   2   1
    1907654 1   0
    1852370 3   1
    39491   3   0
    33039   2   0

<!-- --8<-- [end:merge-head] -->
<!-- --8<-- [start:data-clean] -->

```bash
cd ..
rm -rf taxpasta-tutorial
```

<!-- --8<-- [end:data-clean] -->
