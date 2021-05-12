# exon_intron extractor

## Description
This script parse a gtf file and extract all exons and introns for each transcript in it.

## Usage:
```
usage: extractExon_and_Intron_from_gtf.py [-h] [--gtf GTF]
                                          [--out_exon OUT_EXON]
                                          [--out_intron OUT_INTRON]

optional arguments:
  -h, --help            show this help message and exit
  --gtf GTF             specify a gtf file
  --out_exon OUT_EXON   specify a filename for exon output
  --out_intron OUT_INTRON
                        specify a filename for intron output
```

## output format
Two bed files containing exons and introns separately will be produced.

Each bed files contains 8 columns, the 1 to 6 columns are standard bed file columns,
the additional two columns are gene_name and gene_type, respectively.
