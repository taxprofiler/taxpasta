# Getting Started

In this getting started tutorial we will show you how to generate standardised
taxonomic profiles from the diverse outputs of two popular taxonomic profilers:
[Kraken2](https://ccb.jhu.edu/software/kraken2/) and
[mOTUs](https://motu-tool.org/) using `taxpasta`.

If you want a more detailed walkthrough of _why_ standardising the profiles is
useful, please see the [Deep Dive](deepdive.md) tutorial.

## Preparation

### Software

For this tutorial you will need an internet connection, an [installation of
taxpasta](../index.md#install).

### Data

First we will make a ‘scratch’ directory where we can run the tutorial and
delete again afterwards.

--8<--
tutorial_bash_snippets.md:data-setup
--8<--

We will also need to download some example taxonomic profiles from Kraken2 and
mOTUs. We can download test data from the taxpasta repository using, for
example, `curl` (OSX, Linux) or `wget` (generally Linux Only).

!!! info

    The following test data are from [ancient DNA
    samples](https://doi.org/10.1016/j.cub.2021.09.031) against standard
    databases, thus have a high unclassified rate due to uncharacterised
    environmental contamination and extinct species.

=== "curl"

--8<--
    tutorial_bash_snippets.md:data-curl
--8<--

=== "wget"

--8<--
    tutorial_bash_snippets.md:data-wget
--8<--

We should now see three files with contents in the `taxpasta-tutorial` directory

--8<--
tutorial_bash_snippets.md:data-ls
--8<--

## Profiles

### Raw Output

To begin, let’s look at the contents of the output from each profiler.

=== "mOTUs"

--8<--
    tutorial_bash_snippets.md:motus-head
--8<--

=== "Kraken2"

--8<--
    tutorial_bash_snippets.md:kraken2-head
--8<--

These look quite different. Neither of them is in a nice "pure" tabular format
that is convenient for analysis software or spreadsheet tools such as Microsoft
Excel or LibreOffice Calc to load. They also have different types columns and,
in the case of Kraken2, it has an interesting "indentation" way of showing the
taxonomic rank of each taxon.

## Standardisation and Merging

### taxpasta standardise

This is where `taxpasta` comes to the rescue!

With `taxpasta`, you can standardise and combine profiles into multi-sample
taxon tables for you already at the command-line; rather than having to do this
with custom scripts and a lot of manual data munging.

If you want to standardise a single profile you need three things:

- The name of the taxonomic profiler used to generate the input file
  (`--profiler` or `-p`)
- The requested output file name with a valid suffix that will tell `taxpasta`
  which format to save the output in (`--output` or `-o`)
- The input profile file itself

--8<--
tutorial_bash_snippets.md:standardise
--8<--

Let's look at the result:

--8<--
tutorial_bash_snippets.md:standardise-head
--8<--

This looks much more tidy!

You can see that we did not have to specify any additional column names or other
arguments. `taxpasta` has created a suitable table for you.

### taxpasta merge

What about the more complicated mOTUs case, where we not only have unusual
comment headers but also profiles from _multiple_ samples to be standardised?

In this case, we can instead use `taxpasta merge`, which will both standardise
_and_ merge the profiles of different samples into one for you - all through the
command-line.

Again, We need to specify the profiler, the output name and
format (via the suffix), and the input profiles themselves.

--8<--
tutorial_bash_snippets.md:merge
--8<--

Let's peek at the result.

--8<--
tutorial_bash_snippets.md:merge-head
--8<--

As with Kraken2, this looks much more tabular, and we can see references to
_both_ input files.

!!! danger

    We do not (directly) support merging _across_ different
    classifiers/profilers, as each tool may have its own database, metric, _and_
    taxonomy ID system,. This can risk making naïve assumptions and
    false-positive interpretations, thus `taxpasta` is designed to help
    _prepare_ data for cross-classifier without doing it itself. We rather
    highly recommend doing this mindfully in an exploratory fashion. We provide
    examples of how to do this carefully using R and Python in the corresponding
    [How to merge across
    profilers](../how-tos/how-to-merge-across-profilers.md) section.

    However if you really want this functionality, please let the developers
    know via a [feature
    request](https://github.com/taxprofiler/taxpasta/issues/new?assignees=&labels=enhancement&template=03-feature-request.yml&title=%5BFeature%5D+).

## Additional functionality

- If you want to learn how to use `taxpasta` to add taxonomic names (rather than
  IDs) to your profiles, see [here](../how-tos/how-to-add-names.md).
- Want to customise the sample names in the columns? See
  [here](../how-tos/how-to-customise-sample-names.md).

## Clean Up

Once you’re happy that you’ve completed the tutorial you can clean up your
workspace by removing the tutorial directory.

--8<--
tutorial_bash_snippets.md:data-clean
--8<--
