# TAXPASTA Documentation

_TAXonomic Profile Aggregation and STAndardisation_

## About

The main purpose of taxpasta is to _standardise_ taxonomic profiles created by a
range of bioinformatics tools. We call those tools taxonomic profilers. They
each come with their own particular tabular output format. Across the profilers,
relative abundances can be reported in read counts, fractions, or percentages,
as well as any number of additional columns with extra information. We therefore
decided to take [the lessons learnt](https://xkcd.com/927/) to heart and provide
our own solution to deal with this pasticcio. With taxpasta you can ingest all
of those formats and, at a minimum, output taxonomy identifiers and their
integer counts. Taxpasta can not only standardise profiles but also _merge_ them
across samples for the _same_ profiler into a single table.

### Supported Taxonomic Profilers

Taxpasta currently supports standardisation and generation of comparable
taxonomic tables for:

-   [Bracken](https://ccb.jhu.edu/software/bracken/)
-   [Centrifuge](https://ccb.jhu.edu/software/centrifuge/)
-   [DIAMOND](https://github.com/bbuchfink/diamond)
-   [Kaiju](https://kaiju.binf.ku.dk/)
-   [Kraken2](https://ccb.jhu.edu/software/kraken2/)
-   [KrakenUniq](https://github.com/fbreitwieser/krakenuniq)
-   [MEGAN6](http://www-ab.informatik.uni-tuebingen.de/software/megan6)/[MALT](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/malt/)
-   [MetaPhlAn](https://segatalab.cibio.unitn.it/tools/metaphlan/index.html)
-   [mOTUs](https://motu-tool.org/)

See [supported profilers](/supported_profilers) for more information.

## Install

It's as simple as:

```shell
pip install taxpasta
```

Taxpasta is also available from the [Bioconda](https://bioconda.github.io/)
channel

```shell
conda install -c bioconda taxpasta
```

and thus automatically generated
[Docker](https://quay.io/repository/biocontainers/taxpasta?tab=tags) and
[Singularity](https://depot.galaxyproject.org/singularity/)
[BioContainers](https://biocontainers.pro/) images also exist.

### Optional Dependencies

Taxpasta supports a number of extras that you can install for additional
features; primarily support for additional output file formats. You can install
them by specifying a comma separated list within square brackets, for example,

```shell
pip install 'taxpasta[rich,biom]'
```

-   `rich` provides [rich](https://rich.readthedocs.io/)-formatted command line output and logging.
-   `arrow` supports writing output tables in [Apache Arrow](https://arrow.apache.org/) format.
-   `parquet` supports writing output tables in [Apache Parquet](https://parquet.apache.org/) format.
-   `biom` supports writing output tables in [BIOM](https://biom-format.org/) format.
-   `ods` supports writing output tables in [ODS](https://www.libreoffice.org/discover/what-is-opendocument/) format.
-   `xlsx` supports writing output tables in [Microsoft Excel](https://support.microsoft.com/en-us/office/file-formats-that-are-supported-in-excel-0943ff2c-6014-4e8d-aaea-b83d51d46247) format.
-   `all` includes all of the above.
-   `dev` provides all tools needed for contributing to taxpasta.

## Usage

The main entry point for taxpasta is its command-line interface (CLI). You can interactively
explore the offered commands through the help system.

```shell
taxpasta -h
```

See the [Getting Started](/tutorials/getting-started) tutorial to get familiar with Taxpasta.

Taxpasta currently offers two commands corresponding to the main [use-cases](#about).
You can find out more in the [commands' documentation](/commands).

### Standardise

Since the [supported profilers](#supported-taxonomic-profilers) all produce
their own flavour of tabular output, a quick way to normalize such files, is to
standardise them with taxpasta. You need to let taxpasta know what tool the file
was created by. As an example, let's standardise a MetaPhlAn profile. (You can
find an example file in our [test
data](https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/metaphlan/MOCK_002_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt).)

```shell
curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/metaphlan/MOCK_002_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt

taxpasta standardise -p metaphlan -o standardised.tsv MOCK_002_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt
```

With these minimal arguments, taxpasta produces a two column output consisting of

| taxonomy_id | count |
| ----------- | ----- |
|             |       |

You can count on the second column being integers :wink: Having such a simple
and tidy table should make your downstream analysis much smoother to start out
with. Please, have a look at the full [getting
started](/tutorials/getting-started) tutorial for a more thorough
introduction.

### Merge

Converting single tables is nice, but hopefully you have many shiny samples to
analyze. The `taxpasta merge` command works similarly to `standardise` except
that you provide multiple profiles as input. Grab a few more MOCK examples from
our [test
data](https://github.com/taxprofiler/taxpasta/tree/main/tests/data/metaphlan) and
try it out.

```shell
LOCATION=https://raw.githubusercontent.com/taxprofiler/taxpasta/main/tests/data/metaphlan
curl -O "${LOCATION}/MOCK_001_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt"
curl -O "${LOCATION}/MOCK_002_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt"
curl -O "${LOCATION}/MOCK_003_Illumina_Hiseq_3000_se_metaphlan3-db.metaphlan3_profile.txt"

taxpasta merge -p metaphlan -o merged.tsv MOCK_*.metaphlan3_profile.txt
```

The output of the `merge` command has one column for the taxonomy identifier and
one more column for each input profile. Again, please have a look at the full
[getting started](/tutorials/getting-started) tutorial for a more thorough
introduction.

## Copyright

-   Copyright © 2022, 2023, Moritz E. Beber, Maxime Borry, James A. Fellows
    Yates, and Sofia Stamouli.
-   Free software distributed under the [Apache Software License
    2.0](https://www.apache.org/licenses/LICENSE-2.0).
