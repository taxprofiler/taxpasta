```bash
mkdir taxpasta-tutorial
cd taxpasta-tutorial
```

```bash
## mOTUs
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

## Kraken2
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt
```

<!-- --8<-- [start:taxdump] -->

```bash
curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5
curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
md5sum --check taxdump.tar.gz.md5
mkdir taxdump
tar -C taxdump -xzf taxdump.tar.gz
```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0100    49  100    49    0     0     33      0  0:00:01  0:00:01 --:--:--    33
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0 58.5M    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0  8 58.5M    8 4877k    0     0  2289k      0  0:00:26  0:00:02  0:00:24 2289k 49 58.5M   49 29.0M    0     0  9437k      0  0:00:06  0:00:03  0:00:03 9438k 90 58.5M   90 53.1M    0     0  12.9M      0  0:00:04  0:00:04 --:--:-- 12.9M100 58.5M  100 58.5M    0     0  13.2M      0  0:00:04  0:00:04 --:--:-- 13.9M
    taxdump.tar.gz: OK

<!-- --8<-- [end:taxdump] -->
<!-- --8<-- [start:merge-names] -->

```bash
taxpasta merge -p motus -o dbMOTUs_motus_with_names.tsv --taxonomy taxdump --add-name 2612_pe-ERR5766176-db_mOTU.out 2612_se-ERR5766180-db_mOTU.out
```

    [WARNING] The merged profiles contained different taxa. Additional zeroes were introduced for missing taxa.
    [INFO] Write result to 'dbMOTUs_motus_with_names.tsv'.

<!-- --8<-- [end:merge-names] -->
<!-- --8<-- [start:merge-names-head] -->

```bash
head dbMOTUs_motus_with_names.tsv
```

    taxonomy_id name    2612_pe-ERR5766176-db_mOTU  2612_se-ERR5766180-db_mOTU
    40518   Ruminococcus bromii 20  2
    216816  Bifidobacterium longum  1   0
    1680    Bifidobacterium adolescentis    6   1
    1262820 Clostridium sp. CAG:567 1   0
    74426   Collinsella aerofaciens 2   1
    1907654 Collinsella bouchesdurhonensis  1   0
    1852370 Prevotellamassilia timonensis   3   1
    39491   [Eubacterium] rectale   3   0
    33039   [Ruminococcus] torques  2   0

<!-- --8<-- [end:merge-names-head] -->
<!-- --8<-- [start:samplesheet] -->

```bash
## Get the full paths for each file
ls -1 *mOTU.out > motus_paths.txt

## Construct a sample name based on the filename
sed 's#-db_mOTU.out##g;s#^.*/##g' motus_paths.txt > motus_names.txt

## Create the samplesheet, adding a header, and then adding the samplenames and paths
printf 'sample\tprofile\n' > motus_samplesheet.tsv
paste motus_names.txt motus_paths.txt >> motus_samplesheet.tsv
```

<!-- --8<-- [end:samplesheet] -->
<!-- --8<-- [start:merge-samplesheet] -->

```bash
taxpasta merge -p motus -o dbMOTUs_motus_cleannames.tsv -s motus_samplesheet.tsv
```

    [INFO] Read sample sheet from 'motus_samplesheet.tsv'.
    [WARNING] The merged profiles contained different taxa. Additional zeroes were introduced for missing taxa.
    [INFO] Write result to 'dbMOTUs_motus_cleannames.tsv'.

<!-- --8<-- [end:merge-samplesheet] -->
<!-- --8<-- [start:merge-samplesheet-head] -->

```bash
head dbMOTUs_motus_cleannames.tsv
```

    taxonomy_id 2612_pe-ERR5766176  2612_se-ERR5766180
    40518   20  2
    216816  1   0
    1680    6   1
    1262820 1   0
    74426   2   1
    1907654 1   0
    1852370 3   1
    39491   3   0
    33039   2   0

<!-- --8<-- [end:merge-samplesheet-head] -->

```bash
cd ..
rm -rf taxpasta-tutorial
```
