# How-to add taxa names to output

!!! note

    We follow on from the main [tutorial](/tutorials/getting-started) including
    all files just before the clean up step.

If you wish to have actual human-readable taxon names in your standardised
output, you need to supply 'taxonomy' files. These files are typically called
`nodes.dmp` and `names.dmp`. Most profilers use the [NCBI
taxonomy](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/) files.

Assuming that your current working directory is the `taxpasta-tutorial`
directory, we can download the taxonomy files with the following.

--8<--
bash_snippets.md:taxdump
--8<--

Once downloaded and extracted, you can supply the directory with the taxdump
files to your respective `taxpasta` commands with the `--taxonomy` flag, and
specify which type of taxonomy information to display, e.g., just the name, the
rank, and/or taxonomic lineage.

--8<--
bash_snippets.md:merge-names
--8<--

The merged taxpasta output now looks like:

--8<--
bash_snippets.md:merge-names-head
--8<--

## Clean Up

Don't forget to [remove the tutorial
directory](/tutorials/getting-started#clean-up) if you don't want to keep it for
later use.
