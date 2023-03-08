# Tutorial

In this tutorial we will show you how to generate taxonomic profiles using two popular taxonomic classifers, `Kraken2` and `MetaPhlAn3`, demonstrate how their profile output is very different, and how to make them more easily comparable using `taxpasta`.

The motivation behind `taxpasta` is the problem of ... <!-- TODO background -->

Each profiler has their own advantages and disadvantages, just because one profiler picks up more taxa, does not necessarily mean they are more accurate!

However it is also important to note that different profilers produce additional output columns that may allow you to make more informed decision to the reliability or confidence of each taxonomic identification. So while `taxpasta` is a utility to make comparison between profilers easier to be performed, this does not necessarily mean all comparisons are necessarily valid.

## Preparation

This tutorial assumes you are running this tutorial on a UNIX system (Linux, OSX, or Windows Subsystem for Linux), already have a `conda` installation (such as [`miniconda`]()) on your machine, and have set up your conda to find software from the [bioconda]() bioinformatics package repository. This will allow us to install all the software needed for this tutorial.

<!-- TODO space requiremtns -> software, databases, reads -->

### Software

We are going to generate example taxonomic tables of three small metagenomics samples using `Kraken2` and `MetaPhlan3`, demonstrate how these profiles are difficult to load into a popular statistics programming `R`, and finally show how to standardise the output to make them more comparable with `taxpasta`.

We can install two common taxonomic profilers using conda into a dedicated software environment. To do this, open your terminal, and run the follow conda command.

```bash
conda create -n taxpasta-tutorial -c bioconda kraken2=2.1 metaphlan=3.1 conda-forge::r-base=4.2 conda-forge::r-readr=2.14 taxpasta=0.2
```

We can then activate the environment with

```bash
conda activate taxpasta-tutorial
```

### Data

We will need to download some database and raw read files. We will place this in a 'scratch' directory that you can delete once you complete the tutorial. Make the following directory in a suitable location on your machine, and change into it

```bash
mkdir taxpasta-tutorial
cd taxpasta-tutorial
```

The MetaPhlan conda installation fortunately comes with a database prepackaged, however for Kraken2 we will need to download one. Fortunately [Ben Langmead](https://langmead-lab.org/) provides prebuilt
'standard' metagenomic databases of varying sizes from his [S3 bucket](https://benlangmead.github.io/aws-indexes/k2). We will download the smallest bacterial database provided, for comparability with the bacterial marker genes present in the MetaPhlAn3 database, and is capped at 8GB. We can make a directory for a the database, change into it, and run the following `curl` command to download the database.

```bash
mkdir databases
cd databases
curl https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20221209.tar.gz -o k2_standard_08gb_20221209.tar.gz
```

Once this has successfully downloaded, we can leave this directory, make a new directory, and download three small public DNA sequencing libraries, that we can use to taxonomically classify the reads against the MetaPhlAn3 and Kraken2 databases.

```bash
mkdir reads
cd reads
curl <TODO> -o sample1.fastq.gz
curl <TODO> -o sample2.fastq.gz
curl <TODO> -o sample3.fastq.gz
```

With the software, database, and reads all successfully downloaded and installed, we can generate some taxonomic profiles.

## Generate taxonomic profiles

<!-- save to profiles/ -->

## Taxonomic profile output comparison

## Standardising with taxpasta

To allow us to:

1. More easily load taxonomic profile files into spreadsheet tools like R, pandas, LibreOffice Calc, and/or Microsoft Excel, etc
2. More easily compare the results between the two profilers

We can now run `taxpasta merge` to standardise then join the heterogeneous output of the three sequencing libraries aligned with each profiler.

To run the `merge` subcommand, we need to tell `taxpasta` which classifer or profiler the input files were generated from.

We will generate the standardised output in a tab-separated value (TSV) text file, as this is a very simple and highly portable format that be loaded into the vast majority of spreadsheet and statistics tools. We specify the output format with the prefix at the end of the file name we supply to `--output`.

Finally we supply a list of output files from each of the classifers.

As a whole, the commands for both tools should look like the following

```bash
cd profiles
taxpasta merge --profiler kraken2 --output kraken2_taxon_table.tsv sample1.kreport.txt sample2.kreport.txt sample3.kreport.txt
taxpasta merge --profiler metaphlan --output metaphlan3_taxon_table.tsv sample1.mp3.txt sample2.mp3.txt sample3.mp3.txt
```

You can then view the output by simply running `head` on the two output files

```bash
head kraken2_taxon_table.tsv
```

```text
<!-- TODO -->
```

```bash
head kraken2_taxon_table.tsv
```

```text
<!-- TODO -->
```

> ℹ️ If you wish to produce only per-sample standarised tables, and merge them into a single table yourslf later, use `taxpasta standardise`.

By default, `taxpasta` will simply use the file name as the 'sample name' ID in the headers of each column. If you wish to specify your own sample name for each file, you can specify to `taxpasta` a 'samplesheet' that contains both the paths to the profiles and the sample name. To demonstrate this, we can use a little bit of command-land trickier to generate such a samplesheet.

```bash
cd profiles/

## Get the full paths for each file
ls -1 *kreport.txt > kraken2_paths.txt

## Construct a sample name based on the filename
sed 's#kreport.txt##g' paths.txt > kraken2_names.txt

## Create the samplesheet, adding a header and then adding the samplenames and paths
echo 'sample profile' > kraken2_samplesheet.txt
paste -d " " kraken2_names.txt kraken2_paths.txt >> kraken2_samplesheet.txt
```

To check the file has been created correctly

```bash
cat kraken2_samplesheet.txt
```

We can then re-run `taxpasta` but with the samplesheet rather than the list of files at the end

```bash
taxpasta merge --profiler kraken2 --output kraken2_taxon_table_cleannames.tsv -s kraken2_samplesheet.txt
```

By running `diff` on the output of the earlier and samplesheet `taxpasta merge` , we should see that the output files are identical, except for the 'nicer' sample names in the columns names of the header row.

```bash
diff <(head -n 2 kraken2_taxon_table.tsv) <(head -n 2 kraken2_taxon_table_cleannames.tsv)
```

```text


```

## Taxpasta output comparison

Before comparing two profiles, we would also like to emphasise that it is very important that before you run `taxpasta` for the purposes of comparing the outputs of two or more taxonomic profilers, that you make sure that the _taxonomy ID_ used in the databases the two classfiers are the same, i.e., the taxonomic IDs refer to the same taxon reference sequences. If you do not check that the two profilers use the same taxonomy, you may result in misleading results whereby the counts to the same taxonomic ID in fact refer to different taxa!

To demonstrate how standarising the profiles makes using them easier to compare, we will now instead load the standarised profiles in R, and load them in.

First load R

```bash
R
```

Then within R, again load the `readr` package

```r
library(readr)

profile_kraken2 <- read_tsv('kraken2_taxon_table.tsv')
profile_metaphlan3 <- read_tsv('metaphlan3_taxon_table.tsv')

profile_kraken2
profile_metaphlan3
```

You can see how the command to load the profiles into R was much more straight forward this time around.

Furthermore, <!--TODO CONSIDER JOINING THEM TOGETHER -->

## Clean up

Once you've feel you've completed this tutorial to your satisfaction, you can delete everything by changing out of the directory

```bash
cd ../../
rm -r taxpasta-tutorial
```

Then delete the tutorial's conda environment by running

```bash
conda env list | grep taxpasta-tutorial
```

Giving the path indicated in the result of the previous command to the `rm` command

```bash
rm -r <PATH_TO_TUTORIAL_CONDA_INSTALLATION>
```
