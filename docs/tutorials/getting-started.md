# Getting Started

## Introduction

We will show you how to generate standardised taxonomic profiles from the
diverse outputs of two popular taxonomic profilers:
[Kraken2](https://ccb.jhu.edu/software/kraken2/) and
[mOTUs](https://motu-tool.org/). We demonstrate some benefits of this
standardisation when running downstream analyses on such tables in either the
popular statistical programming language [R](https://www.r-project.org/) or
[Python](https://www.python.org/).

## Preparation

### Software

For this tutorial you will need an internet connection, an [installation of
taxpasta](/#install), and, if you want to follow the R parts, an [installation
of
R](https://rstudio-education.github.io/hopr/starting.html#how-to-download-and-install-r)
itself with the [readr](https://readr.tidyverse.org/) and
[dplyr](https://dplyr.tidyverse.org/) packages from the
[Tidyverse](https://tidyverse.org). Furthermore, we assume a UNIX based
operating system, such as Linux, macOS, or Windows Subsystem for Linux.

To summarise, you will need:


=== "R"

--8<--
    tutorial_r_snippets.md:software
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:software
--8<--

### Data

First we will make a ‘scratch’ directory where we can run the tutorial and
delete again afterwards.

--8<--
tutorial_bash_snippets.md:data-setup
--8<--

We will also need to download some example taxonomic profiles from Kraken2 and
mOTUs. We can download test data from the taxpasta repository using, for
example, `curl` or `wget`.

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

These look quite different and neither of them is in a nice "pure" tabular
format that is convenient for analysis software to load. They also have
different types columns and, in the case of Kraken2, it has an interesting
"indentation" way of showing the taxonomic rank of each taxon.

#### mOTUs

=== "R"

--8<--
    tutorial_r_snippets.md:raw-motus
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:raw-motus
--8<--

That works! At least in terms of reasonable table headers. However, we can see
that there are missing NCBI taxonomy identifiers so there is probably more data
cleaning ahead of us.  Getting to this point took too much effort already to
load what is essentially a simple table. Furthermore, if we are interested in
loading all mOTUs profiles, we would have to load each profile one by one for
each sample, requiring more complicated loops and table join code.

#### Kraken2

And what about the Kraken2 output?

=== "R"

--8<--
    tutorial_r_snippets.md:raw-kraken2
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:raw-kraken2
--8<--

This looks better but if we look at the [Kraken2
documentation](https://github.com/DerrickWood/kraken2/wiki/Manual#distinct-minimizer-count-information),
we can also see that sometimes _extra_ columns may be added to the output,
meaning that our column names wouldn’t always work. So again, not trivial.

### Comparing Output of Different Profilers

What if we wanted to compare the output of the different tools? A nice way to do
this would be to merge the files into one table.

=== "R"

--8<--
    tutorial_r_snippets.md:outer-join
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:outer-join
--8<--

But wait, this doesn't look right at all. We know which sample column we have
from `mOTUs`, but what about the `Kraken` read count column? Also, many of the
columns of the profiles are _not_ shared between the two classifiers/profilers
(see an important note about this [here](#important-caveat)).

Ultimately, we have a lot extra inconsistent differences between different output files. When attempting to merge together the resulting file makes little sense, and thus it's difficult to do any meaningful comparison.

## Standardisation and Merging

### taxpasta standardise

This is where `taxpasta` comes to the rescue!

With `taxpasta`, you can standardise and combine profiles into multi-sample taxon tables
for you already at the command-line (rather than having to do this with custom scripts
and a lot of manual data munging).

If you want to standardise a single profile you need three things:

- The name of of the taxonomic profiler used to generate the input file (`--profiler` or `-p`)
- The requested output file name with a valid suffix that will tell `taxpasta` which format to save the output in
(`--output` or `-o`)
- The input profile file itself

--8<--
tutorial_bash_snippets.md:standardise
--8<--

Let's look at the result:

--8<--
tutorial_bash_snippets.md:standardise-head
--8<--

This looks much more tidy!

=== "R"

--8<--
    tutorial_r_snippets.md:std-kraken2
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:std-kraken2
--8<--


You can see that we did not have to specify any additional column names or other
arguments. Taxpasta has created a suitable table for you.

### taxpasta merge

What about the more complicated mOTUs case, where we not only have unusual
comment headers but also profiles from _multiple_ samples to be standardised?

In this case, we can instead use `taxpasta merge`, which will both standardise
_and_ merge the profiles of different samples into one for you - all
through the command-line. 

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

=== "R"

--8<--
    tutorial_r_snippets.md:merge-motus
--8<--

=== "Python"

--8<--
    tutorial_python_snippets.md:merge-motus
--8<--

You can see we have one `taxonomy_id` column, and two columns each referring to
one of the two samples - all without having to spend time playing with different
arguments for loading the files or additional data transformations.

If you prefer the columns names to be different from just the input filenames, you can also
[provide a sample sheet](/how-tos/how-to-customise-sample-names/) to customise them.

By default, taxpasta uses taxonomy identifiers to merge tables. If you’re
interested in having human-readable taxon names see [How-to add taxon
names](/how-tos/how-to-add-names/).

## Important caveat

!!! tip

    Carefully read our [background
    documentation](/supported_profilers/terminology) on terminology and
    considerations for comparing results from different metagenomic profilers.

You may have noticed that when "standardising" the output from each profiler
that not all columns are retained. This is because each profiler has a different
way of reporting relative abundance, and will produce additional metrics
(represented as additional columns) that allow for better evaluation of the
accuracy or confidence in each identified taxon.

However, as these metrics are _not_ consistent between each profiler, they are
also not comparable, thus in taxpasta we only retain columns that
are conceptually comparable, i.e., taxonomy identifiers and counts.

Please be aware that while taxpasta is a utility to make comparison between
profilers easier to be performed, this does not necessarily mean that all
possible comparisons are necessarily valid - this will depend on a case-by-case
basis of your project!

As an example, for simple presence-and-absence analyses (such as pathogen
screening), taxpasta will be highly suitable for comparing sensitivity of
different tools or reference databases.

## Clean Up

Once you’re happy that you’ve completed the tutorial you can clean up your
workspace by removing the tutorial directory.

--8<--
tutorial_bash_snippets.md:data-clean
--8<--
