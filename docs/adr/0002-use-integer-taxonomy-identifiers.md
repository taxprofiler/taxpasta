# 2. Use Integer Taxonomy Identifiers

Date: 2022-12-23

## Status

Accepted

## Context

Various taxonomic profilers either use supplied or built-in taxonomies. Most
commonly those are either from [NCBI](https://www.ncbi.nlm.nih.gov/taxonomy) or [GTDB](https://gtdb.ecogenomic.org/). In any case, most profilers that we encountered so far use integers to refer to nodes within their taxonomy. This is also the convention for the [TaxonKit's taxdump](https://bioinf.shenwei.me/taxonkit/usage/#create-taxdump) format.

## Decision

We will use integer taxonomy identifiers for our internal standard profile. We
will use the number zero to denote unclassified reads.

## Consequences

All taxonomic profiles need to have their identifiers transformed to integers.
There is some variety in how tools denote unclassified reads. Often they are
given 0 or -1 as the identifier but some tools also provide no value at all. All
of those must be converted to zero. Since pandas cannot handle missing values
for integers, we load identifier columns as string first and then convert them
later.

Another consequence is that if we ever want to attach names or lineages to our
output files, the corresponding taxonomy will have to be loaded separately.
