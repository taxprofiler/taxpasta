---
title: "TAXPASTA: TAXonomic Profile Aggregation and STAndardisation"
tags:
    - bioinformatics
    - metagenomics
    - profiling
    - classification
    - standardisation
    - taxonomy
    - Python
authors:
    - name: Moritz E. Beber
      orcid: 0000-0003-2406-1978
      corresponding: true
      affiliation: 1
    - name: Maxime Borry
      orcid: 0000-0001-9140-7559
      affiliation: 2,3
    - name: Sofia Stamouli
      orcid: 0009-0006-0893-3771
      affiliation: 4
    - name: James A. Fellows Yates
      orcid: 0000-0001-5585-6277
      affiliation: "2, 3, 5"
affiliations:
    - name: Unseen Bio ApS, Fruebjergvej 3, 2100 Copenhagen, Denmark
      index: 1
    - name: Microbiome Sciences Group, Department of Archaeogenetics, Max Planck Institute for Evolutionary Anthropology, Deutscher Platz 6, 04103 Leipzig, Germany
      index: 2
    - name: Associated Research Group of Archaeogenetics, Leibniz Institute for Natural Product Research and Infection Biology Hans Knöll Institute, Adolf-Reichwein-Straße 23, 07745 Jena, Germany
      index: 3
    - name: Department of Microbiology, Tumor and Cell Biology, Karolinska Institute, Solnavägen 1, 171 77 Solna, Sweden
      index: 4
    - name: Department of Paleobiotechnology, Leibniz Institute for Natural Product Research and Infection Biology Hans Knöll Institute, Adolf-Reichwein-Straße 23, 07745 Jena, Germany
      index: 5

date: 2023-05-29
bibliography: paper.bib
---

# Summary

Metagenomic analysis is chiefly concerned with untargeted genetic
characterisation of the taxonomic and functional composition of whole
communities of organisms. Researchers ask questions from metagenomic sequencing
such as 'who is present' (what organisms), and 'what are they doing' (what
functions are they performing)? The nature of this field is such that it
intersects with ecology, medicine, statistics, and bioinformatics. Facilitated
by the development of Next-Generation-Sequencing (NGS), the field often
generates large datasets of many samples and many DNA sequences.

In part, due to the interdisciplinary nature of the field, but also due to the
size of datasets, the task of efficiently identifying the taxonomic 'origin' of
each DNA molecule is a popular and unresolved bioinformatic problem. Thus, there
exists a diverse number of bioinformatics tools in order to analyse metagenomic
sequencing data and produce metagenomic profiles, and researchers will often.
However, most of those tools have invented their own tabular result format,
which complicates downstream analysis and in particular comparison across tools.

TAXPASTA is a standalone command-line tool written in Python that aims to
standardise the diverse range of metagenomic profiler output formats to simple
tabular formats that are easy to use in downstream applications. TAXPASTA
facilitates easier cross-comparison between taxonomic profiling tools without
the need for external or dedicated modules or plugins needed of other
'dedicated' metagenomic profile formats.

# Statement of need

TAXPASTA is a Python package for standardising and aggregating metagenomic
profiles coming from a wide range of tools and databases. It was developed as
part of the nf-core/taxprofiler pipeline [@nf-core/taxprofiler:2023] within the
nf-core community [@ewels_nf-core_2020].

Across profilers, relative abundances can be reported in read counts, fractions,
or percentages, as well as any number of additional columns with extra
information. TAXPASTA can ingest all of those formats and, at a minimum, produce
a standardised output containing taxonomic identifiers and their relative
abundances as integer counts. It can also be used to aggregate profiles from
the same profiler and merge them into a single, standardised table. Having a
singular format facilitates downstream analyses and comparisons.

Primarily, TAXPASTA is a command-line tool that is designed to be used as a
building block in metagenomic analysis workflows. At the time of writing, it was
able to read profiles from nine different profilers, namely Bracken
[@lu_bracken_2017], Centrifuge [@kim_centrifuge_2016], DIAMOND
[@buchfink_sensitive_2021], Kaiju [@menzel_fast_2016], Kraken2
[@wood_improved_2019], KrakenUniq [@breitwieser_krakenuniq_2018], MALT/MEGAN6
[@huson_megan_2016; @vagene_malt_2018], MetaPhlAn
[@blanco-miguez_extending_2023],and mOTUs
[@ruscheweyh_cultivation-independent_2022]. It offered a wide range of output
file formats, such as text-based, tabular formats (CSV[^1], TSV[^2]),
spreadsheets (ODS[^3], XLSX[^4]), optimized binary formats (Apache Arrow[^5] and
Parquet[^6]), and the HDF5-based[^7] BIOM format [@mcdonald_biological_2012].

[^1]: https://en.wikipedia.org/wiki/Comma-separated_values
[^2]: https://en.wikipedia.org/wiki/Tab-separated_values
[^3]: https://en.wikipedia.org/wiki/OpenDocument
[^4]: https://en.wikipedia.org/wiki/Office_Open_XML
[^5]: https://arrow.apache.org/
[^6]: https://parquet.apache.org/
[^7]: https://www.hdfgroup.org/solutions/hdf5/

TAXPASTA is not the first tool to attempt to standardising metagenomic profiles,
but it is by far the most comprehensive in terms of supported profilers and
output formats.

The BIOM format [@mcdonald_biological_2012] was created with a similar intention
of standardising a storage format for microbiome analyses. However, transforming
metagenomic profiles into that format was entirely left to the user. TAXPASTA
is conveniently able to read profiles from a wide range of tools and can also
produce BIOM output.

The QIIME™2 _next-generation microbiome bioinformatics platform_
[@bolyen_reproducible_2019] also maintains internally consistent formats for
storing and processing metagenomic data that new tools can plug into.

Some of the taxonomic profilers also come with scripts to convert their output
into another format but none of them support such a wide range of tools as
taxpasta does.

# Acknowledgements

SS was supported by "Rapid establishment of comprehensive laboratory pandemic
preparedness – RAPID-SEQ". MB and JAFY was supported by the Max Planck Society.
JAFY received funding from the Werner Siemens-Stiftung ("Paleobiotechnology",
awarded to Prof. Pierre Stallforth and Prof. Christina Warinner).

# References
