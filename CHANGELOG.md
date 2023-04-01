# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - (2023-04-01)

### Added

-   Inserted columns with taxonomic information like the name, rank, or lineage of a
    taxon at the beginning of the table rather than the end (#86).

### Fixed

-   Enabled handling of MetaPhlAn profiles with taxonomy identifier -1 and combined all
    unclassified entries into one with ID 0 (#85).
-   Generally increased the tolerance in the compositionality checks. Up to 1% deviation  
    are now allowed; 2% for Bracken profiles (#84).

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
