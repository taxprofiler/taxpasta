# TAXPASTA

|            |                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package    | [![Latest PyPI Version](https://img.shields.io/pypi/v/taxpasta.svg)](https://pypi.org/project/taxpasta/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/taxpasta.svg)](https://pypi.org/project/taxpasta/) [![DOI](https://zenodo.org/badge/499589621.svg)](https://zenodo.org/badge/latestdoi/499589621)                                                                                                     |
| Meta       | [![Apache-2.0](https://img.shields.io/pypi/l/taxpasta.svg)](LICENSE) [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](.github/CODE_OF_CONDUCT.md) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)                                                                                                               |
| Automation | [![GitHub Workflow](https://github.com/taxprofiler/taxpasta/workflows/CI-CD/badge.svg)](https://github.com/taxprofiler/taxpasta/workflows/CI-CD) [![Documentation](https://readthedocs.org/projects/taxpasta/badge/?version=latest)](https://taxpasta.readthedocs.io/en/latest/?badge=latest) [![Code Coverage](https://codecov.io/gh/taxprofiler/taxpasta/branch/dev/graph/badge.svg)](https://codecov.io/gh/taxprofiler/taxpasta) |

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

Taxpasta supports a number of extras that you can install for additional features. You
can install them by specifying a comma separated list within square brackets, for example,

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

## Copyright

-   Copyright © 2022, 2023, Moritz E. Beber, Maxime Borry, James A. Fellows Yates, and
    Sofia Stamouli.
-   Free software distributed under the [Apache Software License
    2.0](https://www.apache.org/licenses/LICENSE-2.0).
