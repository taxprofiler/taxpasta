# How-to Merge Across Profilers

As stated in the main description of the tools and tutorials, `taxpasta` does
not (directly) support merging _across_ different profilers, as each tool may
have its own reference database, taxonomy, and/or abundance metric. This can
risk making naïve assumptions and false-positive interpretations, thus
`taxpasta` is designed to help _prepare_ data for cross-profiler analysis
without doing so itself. We highly recommend doing this mindfully in an
exploratory fashion.

Here we will show you how you can load such standardised profiles into R and
Python in a way that allows you to distinguish between the two tools as
necessary.

## Dependencies

=== "R"

    You will need the following packages and libraries.

    ```r
    install.packages(
        c("readr", "dplyr", "purrr", "tibble", "tidyr"),
        dependencies = TRUE
    )
    ```

=== "Python"

    [Pandas](https://pandas.pydata.org/) is already part of the taxpasta
    installation, so you don't need to install anything further.

## Merging Across Profilers

Assuming you had two files in the same directory, `motus_dbMOTUs.tsv` and
`kraken2_db2.tsv` - both of which are the output from a previous `taxpasta merge` command - you can load them as follows.

=== "R"

    First, create a list of the TSV files.

    ```r
    filelist <- list.files(pattern = "*.tsv")
    ```

    Next, we use the list to create a table with the file names in one column,
    load the contents of each file into a nested column, and finally remove the
    nesting for those contents. If your files were created in wide format (the
    default for `taxpasta`), then we also need to pivot the tables to end up
    with a tidy format. Otherwise, the highlighted lines below won't be
    necessary[^1].

    ```r hl_lines="6-11" linenums="1"
    filelist |>
        as_tibble_col(column_name = "filename") |>
        mutate(
            file_contents = map(
                filename, ~ read_tsv(.x) |>
                    pivot_longer(  # (1)!
                        !matches("taxonomy_id"),
                        names_to = "sample",
                        values_to = "count"
                    ) |>
                    select(taxonomy_id, sample, count)
            )
        ) |>
        unnest(cols = file_contents)
    ```

    1. Remove all of the highlighted lines 6-11, as well as the pipe on line 5
       if your tables are already in long format.

    This will result in a _long_ format table containing four columns:
     `taxonomy_id`, `sample`, `count`, and `filename`.

    [^1]: R code adapted from Claus Wilke's [blog
    post](https://clauswilke.com/blog/2016/06/13/reading-and-combining-many-tidy-data-files-in-r/).

=== "Python"

    First, we iterate over TSV files in the working directory.  Next, we load
    the table from each file into a pandas dataframe. Assuming that those tables
    are in _wide_ format, since that is taxpasta's default, we pivot the tables
    into _long_ format using `melt`. Otherwise, the highlighted part can be
    skipped.  Then, we assign the filename to a new column as an identifier for
    which profiler was used. Lastly, we concatenate all tables into one
    dataframe.

    ```python hl_lines="9-14" linenums="1"
    from pathlib import Path

    import pandas as pd

    tables = []
    for filename in Path().glob("*.tsv"):
        df = (
            pd.read_table(filename)
            .melt(  # (1)!
                id_vars=["taxonomy_id"],
                var_name="sample",
                value_name="count",
                ignore_index=True
            )
            .assign(filename=filename)
        )
        tables.append(df)

    result = pd.concat(tables, ignore_index=True)
    ```

    1. Remove the call to the `melt` method (lines 9-14) if your tables are
       already in long format.

    The `result` is a _long_ format table with for columns: `taxonomy_id`,
    `sample`, `count`, and `filename`.

From here, you can ensure that when you are making comparisons between tools you
are taking the tool and database into account via the `filename` column. Of
course, you may add further columns like `profiler` instead.
