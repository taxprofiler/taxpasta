# How To: Custom sample names

> ℹ️ The examples here follow on from the main [introductory tutorial](tutorial.md) prior the clean up step.

With `taxpasta` you can also customise the sample names that are
displayed in the column header of your table, by creating a samplesheet
that has the sample name you want and paths to the files.

We can generate such a TSV sample sheet with a bit of `bash` trickery.

```bash
## Get the full paths for each file
ls -1 taxpasta-tutorial/*mOTU.out > taxpasta-tutorial/motus_paths.txt

## Construct a sample name based on the filename
sed 's#-db_mOTU.out##g;s#^.*/##g' taxpasta-tutorial/motus_paths.txt > taxpasta-tutorial/motus_names.txt

## Create the samplesheet, adding a header, and then adding the samplenames and paths
printf 'sample\tprofile\n' > taxpasta-tutorial/motus_samplesheet.tsv
paste taxpasta-tutorial/motus_names.txt taxpasta-tutorial/motus_paths.txt >> taxpasta-tutorial/motus_samplesheet.tsv
```

Then instead of giving to `merge` the paths to each of the profiles, we
can provide the samplesheet itself

```bash
taxpasta merge --profiler motus -o taxpasta-tutorial/dbMOTUs_motus_cleannames.tsv -s taxpasta-tutorial/motus_samplesheet.tsv
```

    [INFO] Read sample sheet from 'taxpasta-tutorial/motus_samplesheet.tsv'.
    [WARNING] The merged profiles contained different taxa. Additional zeroes were introduced for missing taxa.
    [INFO] Write result to 'taxpasta-tutorial/dbMOTUs_motus_cleannames.tsv'.
