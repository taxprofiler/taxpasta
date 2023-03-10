# How To: Adding Taxon Names To Standardised Output

> ℹ️ The examples here follow on from the main [introductory tutorial](tutorial.md) prior the clean up step.

If you wish to have actual human-readable taxon names in your
standardised output, you need to supply ‘taxonomy’ files. These files
are typically called `nodes.dmp` and `names.dmp`. Most classifiers/profilers use
the [NCBI
taxonomy](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) files.

> ⚠️ The following `.dmp` files can be very large \>1.8GB when
> uncompressed!

```bash
curl -o taxpasta-tutorial/new_taxdump.zip https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
unzip taxpasta-tutorial/new_taxdump.zip -d taxpasta-tutorial
```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
      0  122M    0 16384    0     0  13050      0  2:44:35  0:00:01  2:44:34 13044
      6  122M    6 7904k    0     0  3627k      0  0:00:34  0:00:02  0:00:32 3627k
     19  122M   19 23.4M    0     0  7535k      0  0:00:16  0:00:03  0:00:13 7535k
     31  122M   31 38.4M    0     0  9364k      0  0:00:13  0:00:04  0:00:09 9363k
     42  122M   42 51.7M    0     0   9.9M      0  0:00:12  0:00:05  0:00:07 10.2M
     47  122M   47 58.6M    0     0  9678k      0  0:00:13  0:00:06  0:00:07 11.8M
     53  122M   53 65.8M    0     0  9361k      0  0:00:13  0:00:07  0:00:06 11.5M
     58  122M   58 72.4M    0     0  9071k      0  0:00:13  0:00:08  0:00:05  9.8M
     62  122M   62 77.1M    0     0  8564k      0  0:00:14  0:00:09  0:00:05 7894k
     65  122M   65 80.2M    0     0  8072k      0  0:00:15  0:00:10  0:00:05 5878k
     67  122M   67 82.9M    0     0  7602k      0  0:00:16  0:00:11  0:00:05 5005k
     70  122M   70 86.5M    0     0  7274k      0  0:00:17  0:00:12  0:00:05 4247k
     74  122M   74 91.2M    0     0  7095k      0  0:00:17  0:00:13  0:00:04 3865k
     79  122M   79 98.1M    0     0  7088k      0  0:00:17  0:00:14  0:00:03 4332k
     86  122M   86  106M    0     0  7188k      0  0:00:17  0:00:15  0:00:02 5387k
     90  122M   90  111M    0     0  7075k      0  0:00:17  0:00:16  0:00:01 5896k
     94  122M   94  115M    0     0  6907k      0  0:00:18  0:00:17  0:00:01 6013k
     96  122M   96  118M    0     0  6683k      0  0:00:18  0:00:18 --:--:-- 5600k
     99  122M   99  121M    0     0  6502k      0  0:00:19  0:00:19 --:--:-- 4843k
    100  122M  100  122M    0     0  6458k      0  0:00:19  0:00:19 --:--:-- 3891k
    Archive:  taxpasta-tutorial/new_taxdump.zip
      inflating: taxpasta-tutorial/citations.dmp
      inflating: taxpasta-tutorial/delnodes.dmp
      inflating: taxpasta-tutorial/division.dmp
      inflating: taxpasta-tutorial/excludedfromtype.dmp
      inflating: taxpasta-tutorial/fullnamelineage.dmp
      inflating: taxpasta-tutorial/gencode.dmp
      inflating: taxpasta-tutorial/host.dmp
      inflating: taxpasta-tutorial/merged.dmp
      inflating: taxpasta-tutorial/names.dmp
      inflating: taxpasta-tutorial/nodes.dmp
      inflating: taxpasta-tutorial/rankedlineage.dmp
      inflating: taxpasta-tutorial/taxidlineage.dmp
      inflating: taxpasta-tutorial/typematerial.dmp
      inflating: taxpasta-tutorial/typeoftype.dmp
      inflating: taxpasta-tutorial/gc.prt

Once downloaded, you can supply these files to your respective
`taxpasta` command with the `--taxonomy` flag, and specify which type of
taxon names to be displayed (e.g., just the name, the rank, and/or
taxonomic lineage).

```bash
taxpasta merge --profiler motus -o taxpasta-tutorial/dbMOTUs_motus_with_names.tsv taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out taxpasta-tutorial/2612_se-ERR5766180-db_mOTU.out --taxonomy taxpasta-tutorial/ --add-name
```

    [WARNING] The merged profiles contained different taxa. Additional zeroes were introduced for missing taxa.
    [INFO] Write result to 'taxpasta-tutorial/dbMOTUs_motus_with_names.tsv'.

The taxpasta now looks like

```bash
head taxpasta-tutorial/dbMOTUs_motus_with_names.tsv
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

## Clean Up
