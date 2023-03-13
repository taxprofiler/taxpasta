```bash
mkdir taxpasta-tutorial
cd taxpasta-tutorial
```

```bash
## mOTUs
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

## Kraken2
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt
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

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    100    49  100    49    0     0     38      0  0:00:01  0:00:01 --:--:--    38

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current

                                     Dload  Upload   Total   Spent    Left  Speed

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

      0 57.8M    0 17376    0     0  13692      0  1:13:49  0:00:01  1:13:48 13681

      8 57.8M    8 4812k    0     0  2169k      0  0:00:27  0:00:02  0:00:25 2168k

     25 57.8M   25 14.8M    0     0  4718k      0  0:00:12  0:00:03  0:00:09 4718k

     42 57.8M   42 24.8M    0     0  6024k      0  0:00:09  0:00:04  0:00:05 6022k

     62 57.8M   62 36.3M    0     0  7159k      0  0:00:08  0:00:05  0:00:03 7447k

     85 57.8M   85 49.2M    0     0  8093k      0  0:00:07  0:00:06  0:00:01  9.9M

    100 57.8M  100 57.8M    0     0  8566k      0  0:00:06  0:00:06 --:--:-- 11.3M

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

    taxonomy_id 2612_pe-ERR5766176-db_mOTU  2612_se-ERR5766180-db_mOTU  name

    40518   20  2   Ruminococcus bromii

    216816  1   0   Bifidobacterium longum

    1680    6   1   Bifidobacterium adolescentis

    1262820 1   0   Clostridium sp. CAG:567

    74426   2   1   Collinsella aerofaciens

    1907654 1   0   Collinsella bouchesdurhonensis

    1852370 3   1   Prevotellamassilia timonensis

    39491   3   0   [Eubacterium] rectale

    33039   2   0   [Ruminococcus] torques

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
