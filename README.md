# TAXPASTA

|            |                                                                                                                                                                                                                                                                                                                                                                               |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package    | [![Latest PyPI Version](https://img.shields.io/pypi/v/taxpasta.svg)](https://pypi.org/project/taxpasta/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/taxpasta.svg)](https://pypi.org/project/taxpasta/) [![Documentation](https://readthedocs.org/projects/taxpasta/badge/?version=latest)](https://taxpasta.readthedocs.io/en/latest/?badge=latest) |
| Meta       | [![Apache-2.0](https://img.shields.io/pypi/l/taxpasta.svg)](LICENSE) [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](.github/CODE_OF_CONDUCT.md) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)                                                         |
| Automation | [![GitHub Workflow](https://github.com/taxprofiler/taxpasta/workflows/CI-CD/badge.svg)](https://github.com/taxprofiler/taxpasta/workflows/CI-CD) [![Code Coverage](https://codecov.io/gh/taxprofiler/taxpasta/branch/master/graph/badge.svg)](https://codecov.io/gh/taxprofiler/taxpasta)                                                                                     |

_TAXonomic Profile Aggregation and STAndardisation_

## About

The main purpose of taxpasta is to _standardise_ taxonomic profiles created by a
range of bioinformatics tools. We call those tools taxonomic profilers. They
each come with their own particular tabular output format. Across the profilers, relative abundances can be reported
in read counts, fractions, or percentages, as well as any number of additional columns with extra
information. We therefore decided to take [the lessons
learnt](https://xkcd.com/927/) to heart and provide our own solution to deal
with this pasticcio. With taxpasta you can ingest all of those formats and, at
a minimum, output taxonomy identifiers and their integer counts.

Taxpasta can not only standardise profiles but also _merge_ them
across samples for the same profiler into a single table. In future, we also intend to offer methods
for forming a _consensus_ for the same sample analyzed by different profilers.

## Install

It's as simple as:

```shell
pip install taxpasta
```

## Copyright

-   Copyright © 2022, Moritz E. Beber, Maxime Borry, James A. Fellows Yates, and
    Sofia Stamouli.
-   Free software distributed under the [Apache Software License
    2.0](https://www.apache.org/licenses/LICENSE-2.0).
