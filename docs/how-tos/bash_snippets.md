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

    100    49  100    49    0     0     33      0  0:00:01  0:00:01 --:--:--    33

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current

                                     Dload  Upload   Total   Spent    Left  Speed

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

      0 57.8M    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0

     14 57.8M   14 8825k    0     0  4125k      0  0:00:14  0:00:02  0:00:12 4123k

     40 57.8M   40 23.3M    0     0  7738k      0  0:00:07  0:00:03  0:00:04 7736k

     56 57.8M   56 32.7M    0     0  8153k      0  0:00:07  0:00:04  0:00:03 8151k

     74 57.8M   74 43.1M    0     0  8663k      0  0:00:06  0:00:05  0:00:01 8998k

     94 57.8M   94 54.5M    0     0  9157k      0  0:00:06  0:00:06 --:--:-- 11.0M

    100 57.8M  100 57.8M    0     0  9264k      0  0:00:06  0:00:06 --:--:-- 11.5M

    taxdump.tar.gz: OK

<!-- --8<-- [end:taxdump] -->
<!-- --8<-- [start:merge-names] -->

```bash
taxpasta merge -p motus -o dbMOTUs_motus_with_names.tsv --taxonomy taxdump --add-name 2612_pe-ERR5766176-db_mOTU.out 2612_se-ERR5766180-db_mOTU.out
```

    [13:53:47] WARNING  The merged profiles        d=594523;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/application/sample_merging_application.py\sample_merging_application.py;;\:d=133637;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/application/sample_merging_application.py#116\116;;\

                        contained different taxa.

                        Additional zeroes were

                        introduced for missing

                        taxa.

               INFO     Write result to 'dbMOTUs_motus_with_names.tsv'. d=221795;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py\merge.py;;\:d=554515;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py#448\448;;\

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

    [13:53:49] INFO     Read sample sheet from 'motus_samplesheet.tsv'. d=301038;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py\merge.py;;\:d=775761;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py#393\393;;\

               WARNING  The merged profiles        d=737336;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/application/sample_merging_application.py\sample_merging_application.py;;\:d=7963;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/application/sample_merging_application.py#116\116;;\

                        contained different taxa.

                        Additional zeroes were

                        introduced for missing

                        taxa.

               INFO     Write result to 'dbMOTUs_motus_cleannames.tsv'. d=913213;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py\merge.py;;\:d=177024;file:///home/moritz/Codebase/taxprofiler/taxpasta/src/taxpasta/infrastructure/cli/merge.py#448\448;;\

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
