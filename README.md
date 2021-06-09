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


# gtf to bed
## Description
This script convert a gtf file into a bed (bed12) file. Each row in the output bed file represents a transcript, 
and the blocks are exons. Currently, only transcripts in protein_coding genes and lncRNAs from autosomal and two sexual chromosomes are included.

## Usage:
```
usage: gtf2bed12.py [-h] -g GTF [-o OUT_BED]

optional arguments:
  -h, --help            show this help message and exit
  -g GTF, --gtf GTF     specify a gtf file
  -o OUT_BED, --out_bed OUT_BED
                        specify a filename for output
```

## output and format
1. one bed file with 12 columns will be produced. The description of bed12 format can be found in [UCSC website](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).
2. one tab-separated file namely "transcript_to_geneName.txt" will also be produced.
