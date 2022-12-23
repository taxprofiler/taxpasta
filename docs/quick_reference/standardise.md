# standardise

```shell
taxpasta standardise --help
```

```text
 Usage: taxpasta standardise [OPTIONS] PROFILE

 Standardise a taxonomic profile (alias: 'standardize').

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    profile      PATH  A file containing a taxonomic profile. [required]                  │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ *  --profiler       -p      [bracken|centrifuge|diamond|ka  The taxonomic profiler used.   │
│                             iju|kraken2|krakenuniq|megan6|  [required]                     │
│                             metaphlan|motus]                                               │
│ *  --output         -o      PATH                            The desired output file. By    │
│                                                             default, the file extension    │
│                                                             will be used to determine the  │
│                                                             output format.                 │
│                                                             [required]                     │
│    --output-format          [TSV|CSV|ODS|XLSX|arrow|parque  The desired output format.     │
│                             t]                              Depending on the choice,       │
│                                                             additional package             │
│                                                             dependencies may apply. Will   │
│                                                             be parsed from the output file │
│                                                             name but can be set            │
│                                                             explicitly.                    │
│                                                             [default: None]                │
│    --help           -h                                      Show this message and exit.    │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```
