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
integer counts.

Taxpasta can not only standardise profiles but also _merge_ them across samples
for the same profiler into a single table. In future, we also intend to offer
methods for forming a _consensus_ for the same sample analyzed by different
profilers.

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

See [supported profilers](supported_profilers/index) for more information.

## Install

It's as simple as:

```shell
pip install taxpasta
```

## Usage

The main entry point for taxpasta is its command-line interface (CLI). You can interactively
explore the offered commands through the help system.

```shell
taxpasta -h
```

Taxpasta currently offers three commands corresponding to the main [use-cases](#about).
You can find out more in the [commands' documentation](commands/index.md).

## Copyright

-   Copyright © 2022, Moritz E. Beber, Maxime Borry, James A. Fellows Yates, and Sofia Stamouli.
-   Free software distributed under the [Apache Software License
    2.0](https://www.apache.org/licenses/LICENSE-2.0).
