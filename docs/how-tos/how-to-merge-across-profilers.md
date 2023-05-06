# How-to Merge Across Profilers

As stated in the main description of the tools and tutorials, `taxpasta`
does not (directly) support merging _across_ different profilers, as each tool
may have its own reference database, taxonomy, and/or abundance metric. This can
risk making naïve assumptions and false-positive interpretations, thus
`taxpasta` is designed to help _prepare_ data for cross-profiler analysis
without doing so itself. We highly recommend doing this mindfully in an
exploratory fashion.

Here we will show you how you can load such standardised profiles into R and
Python in a way that allows you to distinguish between the two tools as
necessary.

## Dependencies

You will need the following packages and libraries.

```r
install.packages(
    c("readr", "dplyr", "purrr", "tibble", "tidyr"),
    dependencies = TRUE
)
```

## Merging Across Profilers

Assuming you had two files in the same directory, `motus_dbMOTUs.tsv` and
`kraken2_db2.tsv` - both of which are the output from a previous `taxpasta merge`
command - you can load them as follows.

First, create a list of the TSV files.

```r
filelist <- list.files(pattern = "*.tsv")
```

Next, we use the list to create a table with the file names in one column, load the contents
of each file into a nested column, and finally remove the nesting for those contents. If your
files were created in wide format (the default for `taxpasta`), then we also need to pivot the
tables to end up with a tidy format. Otherwise, the highlighted lines below won't be necessary[^1].

```r hl_lines="6-11"
filelist |>
    as_tibble_col(column_name = "filename") |>
    mutate(
        file_contents = map(
            filename, ~ read_tsv(.x) |>
                pivot_longer(
                    !matches("taxonomy_id"),
                    names_to = "file",
                    values_to = "value"
                ) |>
                select(taxonomy_id, file, value)
        )
    ) |>
    select(file_contents) |>
    unnest(cols = c(file_contents))
```

This will result in a _long_ format table containing three columns:
`taxonomy_id`, `file`, and `value`.

From here you can ensure that when you are making comparisons between tools you
are taking the tool and database into account via the `file` name column.

[^1]:
    R code adapted from Claus Wilke's [blog
    post](https://clauswilke.com/blog/2016/06/13/reading-and-combining-many-tidy-data-files-in-r/).
