# How-to customise sample names

!!! note

    We follow on from the main [tutorial](/tutorials/getting-started) including all files just before the clean up step.

With `taxpasta` you can also customise the sample names that are
displayed in the column header of your merged table, by creating a sample sheet
that has the sample name you want and paths to the files.

We can generate such a TSV sample sheet with a bit of `bash` trickery or your favourite
spreadsheet program.

Assuming that your current working directory is the `taxpasta-tutorial` directory.

--8<--
bash_snippets.md:samplesheet
--8<--

Then instead of giving to `merge` the paths to each of the profiles, we
can provide the sample sheet itself.

--8<--
bash_snippets.md:merge-samplesheet
--8<--

You can now see that the column headers look a bit better.

--8<--
bash_snippets.md:merge-samplesheet-head
--8<--

## Clean Up

Don't forget to [remove the tutorial directory](/tutorials/getting-started#clean-up) if you don't want to keep it for later use.
