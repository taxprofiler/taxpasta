# History

## Next Release

### Fixed

* Documented _which_ columns are used in final standardised output profiles.

## 0.1.1 (2023-01-28)

### Fixed

* Documentation on where the taxpasta-supported Kaiju output comes from (i.e., 
  kaiju2table rather than Kaiju itself).

### Fixed

* Corrected the assumption that the first two entries in a kraken2 profile are
  always unclassified and root node percentage of abundances. This is not the
  case for profiles where 100% of reads are assigned to taxa. Kraken2 profile
  validation now looks for the `'U'` and `'R'` taxonomy levels explicitly and
  checks their sum.

## 0.1.0 (2023-01-19)

* First release
