# merge

```
$ taxpasta merge --help

 Usage: taxpasta merge [OPTIONS] [PROFILE1 PROFILE2 [...]]

 Standardise and merge two or more taxonomic profiles into a single table.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   profiles      [PROFILE1 PROFILE2 [...]]  Two or more files containing taxonomic profiles. Required unless there is a sample sheet. Filenames will be parsed as sample names.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --profiler            -p            [bracken|centrifuge|kaiju|kraken2|krakenuniq|malt|metaphlan]  The taxonomic profiler used. All provided profiles must come from the same tool! [required]                     │
│    --samplesheet         -s            FILE                                                          A table with a header and two columns: the first column named 'sample' which can be any string and the second   │
│                                                                                                      column named 'profile' which must be a file path to an actual taxonomic abundance profile. If this option is    │
│                                                                                                      provided, any arguments are ignored.                                                                            │
│                                                                                                      [default: None]                                                                                                 │
│    --samplesheet-format                [TSV|CSV|ODS|XLSX|arrow]                                      The file format of the sample sheet. Depending on the choice, additional package dependencies may apply. Will   │
│                                                                                                      be parsed from the sample sheet file name but can be set explicitly.                                            │
│                                                                                                      [default: None]                                                                                                 │
│ *  --output              -o            PATH                                                          The desired output file. By default, the file extension will be used to determine the output format. [required] │
│    --output-format                     [TSV|CSV|ODS|XLSX|arrow|BIOM]                                 The desired output format. Depending on the choice, additional package dependencies may apply. Will be parsed   │
│                                                                                                      from the output file name but can be set explicitly.                                                            │
│                                                                                                      [default: None]                                                                                                 │
│    --wide                    --long                                                                  Output merged abundance data in either wide or (tidy) long format. Ignored when the desired output format is    │
│                                                                                                      BIOM.                                                                                                           │
│                                                                                                      [default: wide]                                                                                                 │
│    --help                -h                                                                          Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
