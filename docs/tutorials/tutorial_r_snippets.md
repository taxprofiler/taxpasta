<!-- --8<-- [start:software] -->

-   Unix terminal (e.g., `bash`)

-   [Python environment with taxpasta](../index.md#install)

-   [R](https://rstudio-education.github.io/hopr/starting.html#how-to-download-and-install-r)

-   Package dependencies

    ```r
    install.packages(c("readr", "dplyr"), dependencies = TRUE)
    ```

<!-- --8<-- [end:software] -->
<!-- --8<-- [start:raw-motus] -->

We can try loading a mOTUs profile into R using the common table reading
function `read_tsv()` from the `readr` package with default arguments.

```r
requireNamespace("readr")
```

    Loading required namespace: readr

```r
profile_motus <- readr::read_tsv("2612_pe-ERR5766176-db_mOTU.out")
```

    Warning: One or more parsing issues, call `problems()` on your data frame for details,
    e.g.:
      dat <- vroom(...)
      problems(dat)

    Rows: 33573 Columns: 1

    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): # git tag version 3.0.3 |  motus version 3.0.3 | map_tax 3.0.3 | ge...

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

You can see we immediately hit an error, as there is a ‘comment’ line at
the top of the mOTUs profile with information on how the profile was
generated.

While such a comment is very useful for reproducibility, to load this we
have to instead add extra options to the function, which makes loading
the table less than smooth for downstream analyses.

```r
profile_motus <- readr::read_tsv("2612_pe-ERR5766176-db_mOTU.out", comment = "#")
```

    Warning: One or more parsing issues, call `problems()` on your data frame for details,
    e.g.:
      dat <- vroom(...)
      problems(dat)

    Rows: 33570 Columns: 3
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): Leptospira alexanderi [ref_mOTU_v3_00001]
    dbl (2): 100053, 0

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

However, once again we hit another error: the column headers are _also_
specified as a comment line… Instead we can try to skip the first two
lines entirely.

```r
profile_motus <- readr::read_tsv("2612_pe-ERR5766176-db_mOTU.out", skip = 2)
```

    Rows: 33571 Columns: 3
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): #consensus_taxonomy
    dbl (2): NCBI_tax_id, 2612_pe-ERR5766176-db_mOTU

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

```r
profile_motus
```

    # A tibble: 33,571 × 3
       `#consensus_taxonomy`                                      NCBI_tax…¹ 2612_…²
       <chr>                                                           <dbl>   <dbl>
     1 Leptospira alexanderi [ref_mOTU_v3_00001]                      100053       0
     2 Leptospira weilii [ref_mOTU_v3_00002]                           28184       0
     3 Chryseobacterium sp. [ref_mOTU_v3_00004]                           NA       0
     4 Chryseobacterium gallinarum [ref_mOTU_v3_00005]               1324352       0
     5 Chryseobacterium indologenes [ref_mOTU_v3_00006]                  253       0
     6 Chryseobacterium artocarpi/ureilyticum [ref_mOTU_v3_00007]         NA       0
     7 Chryseobacterium jejuense [ref_mOTU_v3_00008]                  445960       0
     8 Chryseobacterium sp. G972 [ref_mOTU_v3_00009]                 1805473       0
     9 Chryseobacterium contaminans [ref_mOTU_v3_00010]              1423959       0
    10 Chryseobacterium indologenes [ref_mOTU_v3_00011]                  253       0
    # … with 33,561 more rows, and abbreviated variable names ¹​NCBI_tax_id,
    #   ²​`2612_pe-ERR5766176-db_mOTU`

<!-- --8<-- [end:raw-motus] -->
<!-- --8<-- [start:raw-kraken2] -->

```r
profile_kraken2 <- readr::read_tsv("2612_pe-ERR5766176-db1.kraken2.report.txt")
```

    New names:
    Rows: 43 Columns: 6
    ── Column specification
    ──────────────────────────────────────────────────────── Delimiter: "\t" chr
    (2): U, unclassified dbl (4): 99.97, 627680...2, 627680...3, 0
    ℹ Use `spec()` to retrieve the full column specification for this data. ℹ
    Specify the column types or set `show_col_types = FALSE` to quiet this message.
    • `627680` -> `627680...2`
    • `627680` -> `627680...3`

```r
profile_kraken2
```

    # A tibble: 43 × 6
       `99.97` `627680...2` `627680...3` U        `0` unclassified
         <dbl>        <dbl>        <dbl> <chr>  <dbl> <chr>
     1    0.03          168            0 R          1 root
     2    0.03          168            0 R1    131567 cellular organisms
     3    0.03          168            0 D       2759 Eukaryota
     4    0.03          168            0 D1     33154 Opisthokonta
     5    0.02          152            0 K      33208 Metazoa
     6    0.02          152            0 K1      6072 Eumetazoa
     7    0.02          152            0 K2     33213 Bilateria
     8    0.02          152            0 K3     33511 Deuterostomia
     9    0.02          152            0 P       7711 Chordata
    10    0.02          152            0 P1     89593 Craniata
    # … with 33 more rows

This doesn’t fail to load but unfortunately the column headers look a
bit weird. It seems the Kraken2 file does not include a column header!
In this case we have to specify these ourselves.

```r
profile_kraken2 <- readr::read_tsv(
    "2612_pe-ERR5766176-db1.kraken2.report.txt",
    col_names = c(
        "percent",
        "clade_assigned_reads",
        "direct_assigned_reads",
        "taxonomy_lvl",
        "taxonomy_id",
        "name"
    )
)
```

    Rows: 44 Columns: 6
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (2): taxonomy_lvl, name
    dbl (4): percent, clade_assigned_reads, direct_assigned_reads, taxonomy_id

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

```r
profile_kraken2
```

    # A tibble: 44 × 6
       percent clade_assigned_reads direct_assigned_reads taxonomy_lvl taxon…¹ name
         <dbl>                <dbl>                 <dbl> <chr>          <dbl> <chr>
     1  100.                 627680                627680 U                  0 uncl…
     2    0.03                  168                     0 R                  1 root
     3    0.03                  168                     0 R1            131567 cell…
     4    0.03                  168                     0 D               2759 Euka…
     5    0.03                  168                     0 D1             33154 Opis…
     6    0.02                  152                     0 K              33208 Meta…
     7    0.02                  152                     0 K1              6072 Eume…
     8    0.02                  152                     0 K2             33213 Bila…
     9    0.02                  152                     0 K3             33511 Deut…
    10    0.02                  152                     0 P               7711 Chor…
    # … with 34 more rows, and abbreviated variable name ¹​taxonomy_id

<!-- --8<-- [end:raw-kraken2] -->
<!-- --8<-- [start:outer-join] -->

In the tidyverse flavour of R, we can do this with the `full_join`
function of the `dplyr` package. This form of joining tables includes
all rows both from the left and right table in the resulting table.

```r
requireNamespace("dplyr")
```

    Loading required namespace: dplyr

```r
dplyr::full_join(profile_motus, profile_kraken2)
```

    Error in `dplyr::full_join()`:
    ! `by` must be supplied when `x` and `y` have no common variables.
    ℹ use by = character()` to perform a cross-join.

The error `by must be supplied when x and y have no common variables`
occurs because the column names are not the same between the two tables
for the different profilers’ outputs. We need to specify which column of
the left table should be joined with what column of the right table.

```r
raw_merged_table <- dplyr::full_join(profile_motus, profile_kraken2, by = c("NCBI_tax_id" = "taxonomy_id"))
raw_merged_table
```

    # A tibble: 33,615 × 8
       `#consensus_taxonomy`   NCBI_…¹ 2612_…² percent clade…³ direc…⁴ taxon…⁵ name
       <chr>                     <dbl>   <dbl>   <dbl>   <dbl>   <dbl> <chr>   <chr>
     1 Leptospira alexanderi …  100053       0      NA      NA      NA <NA>    <NA>
     2 Leptospira weilii [ref…   28184       0      NA      NA      NA <NA>    <NA>
     3 Chryseobacterium sp. […      NA       0      NA      NA      NA <NA>    <NA>
     4 Chryseobacterium galli… 1324352       0      NA      NA      NA <NA>    <NA>
     5 Chryseobacterium indol…     253       0      NA      NA      NA <NA>    <NA>
     6 Chryseobacterium artoc…      NA       0      NA      NA      NA <NA>    <NA>
     7 Chryseobacterium jejue…  445960       0      NA      NA      NA <NA>    <NA>
     8 Chryseobacterium sp. G… 1805473       0      NA      NA      NA <NA>    <NA>
     9 Chryseobacterium conta… 1423959       0      NA      NA      NA <NA>    <NA>
    10 Chryseobacterium indol…     253       0      NA      NA      NA <NA>    <NA>
    # … with 33,605 more rows, and abbreviated variable names ¹​NCBI_tax_id,
    #   ²​`2612_pe-ERR5766176-db_mOTU`, ³​clade_assigned_reads,
    #   ⁴​direct_assigned_reads, ⁵​taxonomy_lvl

<!-- --8<-- [end:outer-join] -->
<!-- --8<-- [start:std-kraken2] -->

Now let’s try to load the taxpasta standardised Kraken2 result into R
again.

```r
profile_kraken2_std <- readr::read_tsv("2612_pe-ERR5766176-db1_kraken2.tsv")
```

    Rows: 44 Columns: 2
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    dbl (2): taxonomy_id, count

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

```r
profile_kraken2_std
```

    # A tibble: 44 × 2
       taxonomy_id  count
             <dbl>  <dbl>
     1           0 627680
     2           1      0
     3      131567      0
     4        2759      0
     5       33154      0
     6       33208      0
     7        6072      0
     8       33213      0
     9       33511      0
    10        7711      0
    # … with 34 more rows

<!-- --8<-- [end:std-kraken2] -->
<!-- --8<-- [start:merge-motus] -->

Once again, let’s try loading the standardised and merged mOTUs result
into R.

```r
profile_motus_merged <- readr::read_tsv("dbMOTUs_motus.tsv")
```

    Rows: 37 Columns: 3
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    dbl (3): taxonomy_id, 2612_pe-ERR5766176-db_mOTU, 2612_se-ERR5766180-db_mOTU

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

```r
profile_motus_merged
```

    # A tibble: 37 × 3
       taxonomy_id `2612_pe-ERR5766176-db_mOTU` `2612_se-ERR5766180-db_mOTU`
             <dbl>                        <dbl>                        <dbl>
     1       40518                           20                            2
     2      216816                            1                            0
     3        1680                            6                            1
     4     1262820                            1                            0
     5       74426                            2                            1
     6     1907654                            1                            0
     7     1852370                            3                            1
     8       39491                            3                            0
     9       33039                            2                            0
    10       39486                            1                            0
    # … with 27 more rows

<!-- --8<-- [end:merge-motus] -->
