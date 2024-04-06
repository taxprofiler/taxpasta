# Frequently Asked Questions

Do you have questions? We may have your answer already. If not, please also take a look at the existing [discussion topics](https://github.com/taxprofiler/taxpasta/discussions).

## Why can't I output BIOM format when standardising a single profile?

The [BIOM format](https://biom-format.org/) is currently not a supported output format for the [`taxpasta standardise` command](quick_reference/standardise.md). Attempting to do so will result in an error.
The reason for that is that the BIOM format, in the authors' own words, was "designed to be a general-use format for representing biological sample by observation contingency tables". That means, the format was developed to adequately describe _groups_ of samples.
If you have multiple samples, please use [`taxpasta merge`](quick_reference/merge.md) to combine them into a single BIOM file.
