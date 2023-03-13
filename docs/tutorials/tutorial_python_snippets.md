<!-- --8<-- [start:software] -->

-   Unix terminal (e.g., `bash`)
-   [Python environment with taxpasta](/#install)
-   No additional requirements, since we will make use of
    [pandas](https://pandas.pydata.org/) which is already part of the
    taxpasta installation.

<!-- --8<-- [end:software] -->

```python
# import os
# from pathlib import Path
# from tempfile import mkdtemp
#
# cwd = Path()
# tmp_path = Path(mkdtemp()) / "taxpasta-tutorial" / "python"
# tmp_path.mkdir(parents=True)
# os.chdir(tmp_path)
```

```python
# from urllib.request import urlretrieve
#
# urlretrieve(
    # url="https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out",
    # filename=tmp_path / "2612_pe-ERR5766176-db_mOTU.out"
# )
# urlretrieve(
    # url="https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_se-ERR5766180-db_mOTU.out",
    # filename=tmp_path / "2612_se-ERR5766180-db_mOTU.out"
# )
# urlretrieve(
    # url="https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt",
    # filename=tmp_path / "2612_pe-ERR5766176-db1.kraken2.report.txt"
# )
```

```python
# import subprocess
#
# subprocess.run(["taxpasta", "standardise", "-p", "kraken2", "-o", "2612_pe-ERR5766176-db1_kraken2.tsv", "2612_pe-ERR5766176-db1.kraken2.report.txt"], check=True, capture_output=True)
#
# subprocess.run(["taxpasta", "merge", "-p", "motus", "-o", "dbMOTUs_motus.tsv", "2612_pe-ERR5766180-db_mOTU.out", "2612_se-ERR5766180-db_mOTU.out"], check=True, capture_output=True)
```

<!-- --8<-- [start:raw-motus] -->

We can try loading a mOTUs profile into Python using the common table
reading function `read_table()` from the `pandas` package with default
arguments.

```python
import pandas as pd

profile_motus_2612_pe_raw = pd.read_table("2612_pe-ERR5766176-db_mOTU.out")
```

    ParserError: Error tokenizing data. C error: Expected 1 fields in line 3, saw 3

You can see we immediately hit a `ParserError`, as there is a ‘comment’
line at the top of the mOTUs profile with information on how the profile
was generated.

While such a comment is very useful for reproducibility, to load this we
have to instead add extra options to the function, which makes loading
the table less than smooth for downstream analyses.

```python
profile_motus = pd.read_table(
    "2612_pe-ERR5766176-db_mOTU.out",
    comment="#",
)
profile_motus.head()
```

|     | Leptospira alexanderi \[ref_mOTU_v3_00001\]                  |      100053 |   0 |
| --: | :----------------------------------------------------------- | ----------: | --: |
|   0 | Leptospira weilii \[ref_mOTU_v3_00002\]                      |       28184 |   0 |
|   1 | Chryseobacterium sp. \[ref_mOTU_v3_00004\]                   |         nan |   0 |
|   2 | Chryseobacterium gallinarum \[ref_mOTU_v3_00005\]            | 1.32435e+06 |   0 |
|   3 | Chryseobacterium indologenes \[ref_mOTU_v3_00006\]           |         253 |   0 |
|   4 | Chryseobacterium artocarpi/ureilyticum \[ref_mOTU_v3_00007\] |         nan |   0 |

However, once again we encounter another problem: the column headers are
_also_ specified as a comment line and our first line of data is instead
read as the column headers. We can try to skip the first two lines
entirely to remedy this.

```python
profile_motus = pd.read_table(
    "2612_pe-ERR5766176-db_mOTU.out",
    skiprows=2,
)
profile_motus.head()
```

|     | \#consensus_taxonomy                               | NCBI_tax_id | 2612_pe-ERR5766176-db_mOTU |
| --: | :------------------------------------------------- | ----------: | -------------------------: |
|   0 | Leptospira alexanderi \[ref_mOTU_v3_00001\]        |      100053 |                          0 |
|   1 | Leptospira weilii \[ref_mOTU_v3_00002\]            |       28184 |                          0 |
|   2 | Chryseobacterium sp. \[ref_mOTU_v3_00004\]         |         nan |                          0 |
|   3 | Chryseobacterium gallinarum \[ref_mOTU_v3_00005\]  | 1.32435e+06 |                          0 |
|   4 | Chryseobacterium indologenes \[ref_mOTU_v3_00006\] |         253 |                          0 |

<!-- --8<-- [end:raw-motus] -->
<!-- --8<-- [start:raw-kraken2] -->

```python
profile_kraken2 = pd.read_table("2612_pe-ERR5766176-db1.kraken2.report.txt")
profile_kraken2.head()
```

|     | 99.97 | 627680 | 627680.1 | U   |      0 | unclassified       |
| --: | ----: | -----: | -------: | :-- | -----: | :----------------- |
|   0 |  0.03 |    168 |        0 | R   |      1 | root               |
|   1 |  0.03 |    168 |        0 | R1  | 131567 | cellular organisms |
|   2 |  0.03 |    168 |        0 | D   |   2759 | Eukaryota          |
|   3 |  0.03 |    168 |        0 | D1  |  33154 | Opisthokonta       |
|   4 |  0.02 |    152 |        0 | K   |  33208 | Metazoa            |

This doesn’t fail to load but unfortunately the column headers look a
bit weird. It seems the Kraken2 file does not include a column header!
In this case we have to specify these ourselves.

```python
profile_kraken2 = pd.read_table(
    "2612_pe-ERR5766176-db1.kraken2.report.txt",
    names=[
        "percent",
        "clade_assigned_reads",
        "direct_assigned_reads",
        "taxonomy_lvl",
        "taxonomy_id",
        "name",
    ],
)
profile_kraken2.head()
```

|     | percent | clade_assigned_reads | direct_assigned_reads | taxonomy_lvl | taxonomy_id | name               |
| --: | ------: | -------------------: | --------------------: | :----------- | ----------: | :----------------- |
|   0 |   99.97 |               627680 |                627680 | U            |           0 | unclassified       |
|   1 |    0.03 |                  168 |                     0 | R            |           1 | root               |
|   2 |    0.03 |                  168 |                     0 | R1           |      131567 | cellular organisms |
|   3 |    0.03 |                  168 |                     0 | D            |        2759 | Eukaryota          |
|   4 |    0.03 |                  168 |                     0 | D1           |       33154 | Opisthokonta       |

<!-- --8<-- [end:raw-kraken2] -->
<!-- --8<-- [start:outer-join] -->

With pandas, we can perform such a merge either with the `join` or
`merge` methods and an `"outer"` argument to perform an outer join that
includes all rows both from the left and right table in the resulting
table. The `join` method works best when joining tables on their
indices. In our case, the indices are not meaningful for the join
operation as they are simple integer ranges. We will use the `merge`
method instead.

```python
profile_motus.merge(profile_kraken2, how="outer")
```

    MergeError: No common columns to perform merge on. Merge options: left_on=None, right_on=None, left_index=False, right_index=False

The `MergeError` occurs because the column names are not the same
between the two tables for the different profilers’ outputs. Instead, we
need to specify which column of the left table should be joined with
what column of the right table. The `merge` method allows us to do so.

```python
raw_merged_table = profile_motus.merge(
    profile_kraken2,
    how="outer",
    left_on="NCBI_tax_id",
    right_on="taxonomy_id",
)
raw_merged_table.sample(10)
```

|       | \#consensus_taxonomy                                              | NCBI_tax_id | 2612_pe-ERR5766176-db_mOTU | percent | clade_assigned_reads | direct_assigned_reads | taxonomy_lvl | taxonomy_id | name |
| ----: | :---------------------------------------------------------------- | ----------: | -------------------------: | ------: | -------------------: | --------------------: | -----------: | ----------: | ---: |
| 33034 | Spirosoma endophyticum \[ref_mOTU_v3_11717\]                      |      662367 |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
| 23891 | Neorhizobium galegae \[ref_mOTU_v3_00935\]                        |         399 |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
|  5186 | Actinobacteria species incertae sedis \[ext_mOTU_v3_15937\]       |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
| 18713 | Acidobacteria species incertae sedis \[ext_mOTU_v3_29464\]        |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
|  3049 | Flavobacteriaceae species incertae sedis \[meta_mOTU_v3_13750\]   |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
|  5551 | Clostridiales species incertae sedis \[ext_mOTU_v3_16302\]        |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
| 19547 | Clostridiales species incertae sedis \[ext_mOTU_v3_30298\]        |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
| 28261 | Clostridium collagenovorans \[ref_mOTU_v3_06789\]                 |       29357 |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
|  2265 | Alphaproteobacteria species incertae sedis \[meta_mOTU_v3_12884\] |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |
| 21849 | Clostridiales species incertae sedis \[ext_mOTU_v3_32600\]        |         nan |                          0 |     nan |                  nan |                   nan |          nan |         nan |  nan |

<!-- --8<-- [end:outer-join] -->
<!-- --8<-- [start:std-kraken2] -->

Now let’s try to load the taxpasta standardised Kraken2 result into
Python again.

```python
profile_kraken2_std = pd.read_table("2612_pe-ERR5766176-db1_kraken2.tsv")
profile_kraken2_std.head()
```

|     | taxonomy_id |  count |
| --: | ----------: | -----: |
|   0 |           0 | 627680 |
|   1 |           1 |      0 |
|   2 |      131567 |      0 |
|   3 |        2759 |      0 |
|   4 |       33154 |      0 |

<!-- --8<-- [end:std-kraken2] -->
<!-- --8<-- [start:merge-motus] -->

Once again, let’s try loading the standardised and merged mOTUs result
into Python.

```python
profile_motus_merged = pd.read_table("dbMOTUs_motus.tsv")
profile_motus_merged.head()
```

|     | taxonomy_id | 2612_pe-ERR5766176-db_mOTU | 2612_se-ERR5766180-db_mOTU |
| --: | ----------: | -------------------------: | -------------------------: |
|   0 |       40518 |                         20 |                          2 |
|   1 |      216816 |                          1 |                          0 |
|   2 |        1680 |                          6 |                          1 |
|   3 | 1.26282e+06 |                          1 |                          0 |
|   4 |       74426 |                          2 |                          1 |

<!-- --8<-- [end:merge-motus] -->

```python
# from shutil import rmtree

# os.chdir(cwd)
# rmtree(tmp_path)
```
