Tutorial
================
James A. Fellows Yates

## Introduction

This tutorial will show you how to generate standardised taxonomic
profiles from the heterogeneous output of two popular taxonomic
profilers: [`Kraken2`](https://ccb.jhu.edu/software/kraken2/) and
[`mOTUs`](https://motu-tool.org/), and then demonstrate some of the
benefits of this standardisation when running downstream analyses on
such tables in the popular data science programming language
[`R`](https://www.r-project.org/).

## Preparation

### Software

For this tutorial you will need an internet connection, `taxpasta`
already [installed](/index), and R with the `readr` and `dplyr` packages
from the [Tidyverse](https://tidyverse.org) set of packages installed,
and a UNIX based operating system (Linux, OSX or Windows Subsystem for
Linux).

To summarise you will need:

-   Unix terminal (e.g. `bash`)
-   `taxpasta`
-   `R`
    -   `readr` package
    -   `dplyr` package

### Data

First we will make a ‘scratch’ directory where we can run all the
tutorial and delete the files after.

``` bash
mkdir taxpasta-tutorial
```

We will also need to download some example taxonomic profiles from
`Kraken2` and `mOTUs`. If you’re on UNIX a machine we can download some
test data from the taxpasta repository.

``` bash
## mOTUs
curl -o taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out 
curl -o taxpasta-tutorial/2612_se-ERR5766180-db_mOTU.out https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

## Kraken2
curl -o taxpasta-tutorial/2612_pe-ERR5766176-db1.kraken2.report.txt https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt 
```

We should now see three files with contents in the `taxpasta-tutorial`
directory

``` bash
ls -l taxpasta-tutorial/*
```

## Tutorial

### Raw classifer output

To begin, we can try loading a `mOTUs` profile into R using a common and
‘default’ table reading command, `read_tsv()` from the `readr` package.

``` r
library(readr)

profile_motus_2612_pe_raw <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out")
```

    Warning: One or more parsing issues, see `problems()` for details

    Rows: 33573 Columns: 1
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): # git tag version 3.0.3 |  motus version 3.0.3 | map_tax 3.0.3 | ge...

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

You can see we immediately hit an error, as there is a ‘comment’ line at
the top of the profile with information on how the profile was
generated.

While this is very nice for reproducibility, to load this we have to
instead add extra options to the function, which makes loading the table
less than smooth for downstream analyses.

``` r
profile_motus_2612_pe_raw <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out", comment = "#")
```

    Warning: One or more parsing issues, see `problems()` for details

    Rows: 33570 Columns: 3
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): Leptospira alexanderi [ref_mOTU_v3_00001]
    dbl (2): 100053, 0

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

However, once again we hit another error - the column headers are *also*
specified as a comment line…

Instead we can try to skip the first two tool information lines

``` r
profile_motus_2612_pe_raw <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out", skip = 2)
```

    Rows: 33571 Columns: 3
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): #consensus_taxonomy
    dbl (2): NCBI_tax_id, 2612_pe-ERR5766176-db_mOTU

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
profile_motus_2612_pe_raw
```

    # A tibble: 33,571 × 3
       `#consensus_taxonomy`                            NCBI_tax_id `2612_pe-ERR57…`
       <chr>                                                  <dbl>            <dbl>
     1 Leptospira alexanderi [ref_mOTU_v3_00001]             100053                0
     2 Leptospira weilii [ref_mOTU_v3_00002]                  28184                0
     3 Chryseobacterium sp. [ref_mOTU_v3_00004]                  NA                0
     4 Chryseobacterium gallinarum [ref_mOTU_v3_00005]      1324352                0
     5 Chryseobacterium indologenes [ref_mOTU_v3_00006]         253                0
     6 Chryseobacterium artocarpi/ureilyticum [ref_mOT…          NA                0
     7 Chryseobacterium jejuense [ref_mOTU_v3_00008]         445960                0
     8 Chryseobacterium sp. G972 [ref_mOTU_v3_00009]        1805473                0
     9 Chryseobacterium contaminans [ref_mOTU_v3_00010]     1423959                0
    10 Chryseobacterium indologenes [ref_mOTU_v3_00011]         253                0
    # … with 33,561 more rows

This now works! However we feel getting this to work takes much too
effort to simply load what is essentially a simple table.

Furthermore, we would have to load each profile one by one for each
sample, requiring more complicated loops and table join code.

Now lets try loading the `Kraken2` output.

``` r
profile_kraken2_2612_pe_raw <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db1.kraken2.report.txt")
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

``` r
profile_kraken2_2612_pe_raw
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

This doesn’t fail to load, but unfortunately the column headers look a
bit wierd… it seems the Kraken2 ‘table’ file does not include a column
header! In this case we have to specify these ourselves..

``` r
profile_kraken2_2612_pe_raw <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db1.kraken2.report.txt", col_names = c("percent", "clade_assigned_reads", "direct_assigned_reads", "taxonomy_lvl", "taxonomy_id", "name"))
```

    Rows: 44 Columns: 6
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (2): taxonomy_lvl, name
    dbl (4): percent, clade_assigned_reads, direct_assigned_reads, taxonomy_id

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
profile_kraken2_2612_pe_raw
```

    # A tibble: 44 × 6
       percent clade_assigned_reads direct_assigned_… taxonomy_lvl taxonomy_id name 
         <dbl>                <dbl>             <dbl> <chr>              <dbl> <chr>
     1  100.                 627680            627680 U                      0 uncl…
     2    0.03                  168                 0 R                      1 root 
     3    0.03                  168                 0 R1                131567 cell…
     4    0.03                  168                 0 D                   2759 Euka…
     5    0.03                  168                 0 D1                 33154 Opis…
     6    0.02                  152                 0 K                  33208 Meta…
     7    0.02                  152                 0 K1                  6072 Eume…
     8    0.02                  152                 0 K2                 33213 Bila…
     9    0.02                  152                 0 K3                 33511 Deut…
    10    0.02                  152                 0 P                   7711 Chor…
    # … with 34 more rows

This looks better, but if we see the [Kraken2
documentation](https://github.com/DerrickWood/kraken2/wiki/Manual#distinct-minimizer-count-information)
we can also see that sometimes *extra* columns can be added when certain
flags are given, meaning that our column names wouldn’t always work.

So again, not trivial.

### Comparing raw output of different classifiers

What if we wanted to compare the output of the different tools? A nice
way to do this would be to merge the files into one table.

In the tidyverse flavour of R, we would do this with the `full_join`
function of the `dplyr` package.

``` r
library(dplyr)
```


    Attaching package: 'dplyr'

    The following objects are masked from 'package:stats':

        filter, lag

    The following objects are masked from 'package:base':

        intersect, setdiff, setequal, union

``` r
full_join(profile_motus_2612_pe_raw, profile_kraken2_2612_pe_raw)
```

    Error in `full_join()`:
    ! `by` must be supplied when `x` and `y` have no common variables.
    ℹ use by = character()` to perform a cross-join.

The error `by must be supplied when x and y have no common variables.`
is because the column names are not the same between the two tables for
the different classifer’s outputs.

``` r
raw_merged_table <- full_join(profile_motus_2612_pe_raw, profile_kraken2_2612_pe_raw, by = c("NCBI_tax_id" = "taxonomy_id"))
raw_merged_table
```

    # A tibble: 33,615 × 8
       `#consensus_taxonomy`   NCBI_tax_id `2612_pe-ERR57…` percent clade_assigned_…
       <chr>                         <dbl>            <dbl>   <dbl>            <dbl>
     1 Leptospira alexanderi …      100053                0      NA               NA
     2 Leptospira weilii [ref…       28184                0      NA               NA
     3 Chryseobacterium sp. […          NA                0      NA               NA
     4 Chryseobacterium galli…     1324352                0      NA               NA
     5 Chryseobacterium indol…         253                0      NA               NA
     6 Chryseobacterium artoc…          NA                0      NA               NA
     7 Chryseobacterium jejue…      445960                0      NA               NA
     8 Chryseobacterium sp. G…     1805473                0      NA               NA
     9 Chryseobacterium conta…     1423959                0      NA               NA
    10 Chryseobacterium indol…         253                0      NA               NA
    # … with 33,605 more rows, and 3 more variables: direct_assigned_reads <dbl>,
    #   taxonomy_lvl <chr>, name <chr>

But wait, this doesn’t look right at all. We know which sample column we
have from `mOTUs`, but what about the `Kraken` read count column? Also
many of the columns of the profiles are *not* shared between the two
profilers (see an important note about this [here](#important-caveat)),
so we have a lot of ‘cruft’, and really the resulting file makes no
sense, as you can’t do any proper comparison.

### taxpasta standardise

But this is where `taxpasta` comes to the rescue!

With `taxpasta`, we can already standardised and make multi-sample taxon
tables for you at the command line level (e.g., immediately after
profiling), rather than having to do this with custom scripts and a lot
of manual munging.

If you want to standardise a single sample, you just need to specify the
profiler of the input file, the output file name (with a valid suffix,
which will tell `taxpasta` which format to save the output), and finally
the the profile itself.

``` bash
taxpasta standardise --profiler kraken2 -o taxpasta-tutorial/2612_pe-ERR5766176-db1_kraken2.tsv taxpasta-tutorial/2612_pe-ERR5766176-db1.kraken2.report.txt
```

Now lets try to load the `taxpasta` standardised `Kraken2` result into
`R` again…

``` r
profile_kraken2_2612_pe_standardised <- read_tsv("taxpasta-tutorial/2612_pe-ERR5766176-db1_kraken2.tsv")
```

    Rows: 44 Columns: 2
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    dbl (2): taxonomy_id, count

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
profile_kraken2_2612_pe_standardised
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

You can see we did not have to specify any additional column names or
other loading parameters, `taxpasta` has done it for you.

### taxpasta merge

But what about the more complicated `mOTUs` case, where we have unusual
comment headers, and also multiple samples?

In this case we can instead use `taxpasta merge`, which will both
standardise *and* stick the profiles of different samples into one for
you - again all the command line. Once again, we just need to specify
the profiler, the output name and format (via the suffix), and the
profile itself.

``` bash
taxpasta merge --profiler motus -o taxpasta-tutorial/dbMOTUs_motus.tsv taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out taxpasta-tutorial/2612_se-ERR5766180-db_mOTU.out
```

Once again, lets try loading the `taxpasta` standardised and merged
`mOTUs` result into `R` again…

``` r
profile_motus_standardised <- read_tsv("taxpasta-tutorial/dbMOTUs_motus.tsv")
```

    Rows: 37 Columns: 4
    ── Column specification ────────────────────────────────────────────────────────
    Delimiter: "\t"
    chr (1): name
    dbl (3): taxonomy_id, 2612_pe-ERR5766176-db_mOTU, 2612_se-ERR5766180-db_mOTU

    ℹ Use `spec()` to retrieve the full column specification for this data.
    ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

``` r
profile_motus_standardised
```

    # A tibble: 37 × 4
       taxonomy_id `2612_pe-ERR5766176-db_mOTU` `2612_se-ERR5766180-db_mOTU` name   
             <dbl>                        <dbl>                        <dbl> <chr>  
     1       40518                           20                            2 Rumino…
     2      216816                            1                            0 Bifido…
     3        1680                            6                            1 Bifido…
     4     1262820                            1                            0 Clostr…
     5       74426                            2                            1 Collin…
     6     1907654                            1                            0 Collin…
     7     1852370                            3                            1 Prevot…
     8       39491                            3                            0 [Eubac…
     9       33039                            2                            0 [Rumin…
    10       39486                            1                            0 Dorea …
    # … with 27 more rows

You can see here now we have one `taxonomy_id` column, and two columns
each referring to each of the samples - and all without having to spend
time playing with different parameters and arguments for loading the
files.

By default `taxpasta` uses taxonomy IDs to merge tables. If you’re
interested in having human-readable taxon names see
[below](#adding-taxon-names).

### Comparing standardised output of different classifiers

<!-- TODO UPDATE AFTER COLUM NNAME BUG FIX FOR STANDARDISE OLUMN EADER-->

We can also now more easily merge the tables across the two profilers,
again with the join function - but without any extra specifications, as
all the standardised taxonomic tables now share common column header
names.

``` r
standardised_merged_table <- full_join(profile_motus_standardised, profile_kraken2_2612_pe_standardised)
```

    Joining, by = "taxonomy_id"

``` r
standardised_merged_table
```

    # A tibble: 80 × 5
       taxonomy_id `2612_pe-ERR5766176-db_mOTU` `2612_se-ERR5766180-db…` name  count
             <dbl>                        <dbl>                    <dbl> <chr> <dbl>
     1       40518                           20                        2 Rumi…    NA
     2      216816                            1                        0 Bifi…    NA
     3        1680                            6                        1 Bifi…    NA
     4     1262820                            1                        0 Clos…    NA
     5       74426                            2                        1 Coll…    NA
     6     1907654                            1                        0 Coll…    NA
     7     1852370                            3                        1 Prev…    NA
     8       39491                            3                        0 [Eub…    NA
     9       33039                            2                        0 [Rum…    NA
    10       39486                            1                        0 Dore…    NA
    # … with 70 more rows

### Important caveat

You may have noticed that when ‘standardising’ the output from each
classifier, that not all columns are retained. This is because each
profiler has a different way of making taxonomic classification, and
will produce additional metrics (represented as additional columns) that
allow for better evaluation of the accuracy or confidence in each hit.

However, as these metrics are *not* consistent between each profiler,
they are are not comparable between each other, thus in `taxpasta` we
only retain columns that are conceptually comparable - i.e., raw read
counts.

However you must be aware that *raw read counts* may not always be an
accurate representation of a metagenomic *profile* where an abundance
estimate is mathematically made.

So please be aware that while `taxpasta` is a utility to make comparison
between profilers easier to be performed, this does not necessarily mean
all comparisons are necessarily valid - this will depend on a
case-by-case basis of your project!

For example, for simple presence-and-absence analyses (such as pathogen
screening), taxpasta will be highly suitable for comparing sensitivity
of different tools/databases (providing downstream genomic-level
analyses is carried out to confirm the hit). However using the output
from taxpasta won’t be immediately suitable for differential abundance
analysis in microbial ecology without further conversion of the raw-read
counts to abundance estimates.

## Extras

### Custom sample names

With `taxpasta` you can also customise the sample names that are
displayed in the column header of your table, by creating a samplesheet
that has the sample name you want and paths to the files.

We can generate such a TSV sample sheet with a bit of `bash` trickery.

``` bash
## Get the full paths for each file
ls -1 taxpasta-tutorial/*mOTU.out > taxpasta-tutorial/motus_paths.txt

## Construct a sample name based on the filename
sed 's#-db_mOTU.out##g;s#^.*/##g' taxpasta-tutorial/motus_paths.txt > taxpasta-tutorial/motus_names.txt

## Create the samplesheet, adding a header, and then adding the samplenames and paths
printf 'sample\tprofile\n' > taxpasta-tutorial/motus_samplesheet.tsv
paste taxpasta-tutorial/motus_names.txt taxpasta-tutorial/motus_paths.txt >> taxpasta-tutorial/motus_samplesheet.tsv
```

Then instead of giving to `merge` the paths to each of the profiles, we
can provide the samplesheet itself

``` bash
taxpasta merge --profiler motus -o taxpasta-tutorial/dbMOTUs_motus_cleannames.tsv -s taxpasta-tutorial/motus_samplesheet.tsv
```

### Adding taxon names

If you wish to have actual human-readable taxon names in your
standardised output, you need to supply ‘taxonomy’ files. These files
are typically called `nodes.dmp` and `names.dmp`. Most profilers use the
[NCBI taxonomy](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)
files.

> ⚠️ The following `.dmp` files can be very large \>1.8GB when
> uncompressed!

``` bash
curl -o taxpasta-tutorial/new_taxdump.zip https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
unzip taxpasta-tutorial/new_taxdump.zip -d taxpasta-tutorial
```

Once downloaded, you can supply these files to your respective
`taxpasta` command with the `--taxonomy` flag, and specify which type of
taxon names to be displayed (e.g., just the name, the rank, and/or
taxonomic lineage).

``` bash
taxpasta merge --profiler motus -o taxpasta-tutorial/dbMOTUs_motus.tsv taxpasta-tutorial/2612_pe-ERR5766176-db_mOTU.out taxpasta-tutorial/2612_se-ERR5766180-db_mOTU.out --taxonomy taxpasta-tutorial/ --add-name
```

This would produce output like so

``` text
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
```

## Clean Up

Once you’re happy you’ve completed the tutorial you can clean up your
workspace by simply running

``` bash
rm -r taxpasta-tutorial
```
