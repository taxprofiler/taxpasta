# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

-   Repaired the logic for adding taxonomic information to the output table (#139).

## [0.6.0] - (2023-09-10)

### Added

-   Added an option `--ignore-errors` to the `taxpasta merge` command. This allows
    ignoring individual profiles that cause errors, like empty profiles (#136).

### Changed

-   Created a special error message for empty profiles, making the cause of the error
    much clearer (#136).
-   Internal restructuring of input validation and transformation services (#136).

## [0.5.0] - (2023-08-24)

### Added

-   Added classifier support for KMCP profiles (#129).
-   Added a command-line option `--add-rank-lineage` to the `standardise` and
    `merge` commands, which inserts a new column `rank_lineage` to results that
    contains semi-colon-separated strings with the ranks (#130).
-   Added a taxonomy table to the BIOM output format when the `--taxonomy` option is
    used (#134).

### Changed

-   Reversed the order of lineages printed to output files (#131).

## [0.4.1] - (2023-07-13)

### Fixed

-   Forced reading the `duplicates` and `coverage` columns of KrakenUniq profiles as
    float (#123).

## [0.4.0] - (2023-07-02)

### Added

-   Provided curl commands in the intro to quickly fetch example files to try out (#97).
-   Added new tutorial on merging across classifiers, and warnings why taxpasta
    does not currently do this natively (#98).
-   Added classifier support for ganon report files (#109).

### Changed

-   Made profile validation stricter, such that providing an input from another
    than the chosen profiler will usually result in an error (#101). The only
    exception is that Kraken2 standard profiles can be provided to the
    Centrifuge reader, and vice versa, since they are identical in format.

### Fixed

-   Fixed a few broken internal links (#89).
-   Simplified getting started tutorial and moved original to complex tutorial (#95).
-   Improved help text for `--output-format` option to clearly state that it disables
    any automatic detection of the output file format (#96).
-   Extended the MetaPhlAn profile reader to support version 3 & 4 profiles (#107).

## [0.3.0] - (2023-04-01)

### Added

-   Inserted columns with taxonomic information like the name, rank, or lineage of a
    taxon at the beginning of the table rather than the end (#86).

### Fixed

-   Enabled handling of MetaPhlAn profiles with taxonomy identifier -1 and combined all
    unclassified entries into one with ID 0 (#85).
-   Generally increased the tolerance in the compositionality checks. Up to 1%
    deviation are now allowed; 2% for Bracken profiles (#84).

## [0.2.3] - (2023-03-12)

### Fixed

-   Fixed the version string according to hatch-vcs output (#74).
-   Increased the tolerance when comparing floats in the Bracken profile validation
    (#76).

## [0.2.2] - (2023-03-08)

### Fixed

-   Fixed how the `taxopy.TaxDb` is loaded. It was previously deleting local files and
    downloading a new copy from NCBI instead (#67).

## [0.2.1] - (2023-03-01)

### Fixed

-   Handled metaphlan profiles with unclassified taxa in the lineage (#61).

## [0.2.0] - (2023-02-23)

### Added

-   Created command line options to expand the standard profile with name, rank,
    and/or lineage taxonomic information (#60).

### Fixed

-   Made the Krakenuniq reader more accepting (#57).
-   Documented _which_ columns are used in final standardised output profiles.

## [0.1.1] - (2023-01-28)

### Fixed

-   Documentation on where the taxpasta-supported Kaiju output comes from (i.e.,
    `kaiju2table` rather than Kaiju itself) (#54).
-   Corrected the assumption that the first two entries in a kraken2 profile are
    always unclassified and root node percentage of abundances. This is not the
    case for profiles where 100% of reads are assigned to taxa. Kraken2 profile
    validation now looks for the `'U'` and `'R'` taxonomy levels explicitly and
    checks their sum.

## [0.1.0] - (2023-01-19)

-   First release
