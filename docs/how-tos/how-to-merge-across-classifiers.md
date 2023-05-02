# How-to merge across classifiers

As stated in the the main description of the tools and the tutorials `taxpasta` does not (directly) support merging _across_ different classifiers/profilers, as each tool may have it's own database and metric.
This can risk making naïve assumptions and false-positive interpretations, thus `taxpasta` is designed to help _prepare_ data for cross-classifier without doing it itself.
We rather highly recommend doing this mindfully in an exploratory fashion.

Here we will show you how you can load such standardised profiles into R and Python in a way that allows you to distinguish between the two tools as necessary.

## Dependencies

You will need the following packages and libraries.

```r
install.packages(c("readr", "dplyr", "purrr", "tibble", "tidyr"), dependencies = TRUE)
```

## Merging Across Classifiers

Assuming you had two files in the same directory, "motus_dbMOTUs.tsv" and "kraken2_db2.tsv" - both of which are output from `taxpasta merge` - you can load them as follows:

```r
## Get list of files
filelist <- list.files(pattern = "*.tsv")

## Convert list to a table, load contents of each file in a new nested column.
## Within each, pivot to a long format table retaining filenames.
## finally un-nest to unpack to have all tables in one.
filelist |>
    as_tibble_col(column_name = "filename") |>
    mutate(
        file_contents = map(filename, ~ read_tsv(.x) |>
                                            pivot_longer(
                                                !matches("taxonomy_id"),
                                                names_to = "file",
                                                values_to = "value") |>
                                            select(taxonomy_id, file, value))) |>
    select(file_contents) |>
    unnest(cols = c(file_contents))
```

This will result in a _long_ format table containing three columns: `taxonomy_id`, `file`, and `value`.

From here you can ensure that when you are making comparisons between tools you are taking the tool and database into account via the `file` name column.

_R code adapted from Claus Wilke's [blog post](https://clauswilke.com/blog/2016/06/13/reading-and-combining-many-tidy-data-files-in-r/)_.
