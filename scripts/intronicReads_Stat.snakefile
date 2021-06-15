#

rule extract_intronic_region:
  input:
    input/gencode.v38.annotation.gtf
  output:
    exon="output/gencode_v38_exon.bed"
    intron="output/gencode_v38_intron.bed"
    generange="output/geneRange.bed"
  shell:
    "python src/extractExon_and_Intron_from_gtf.py3 --gtf {input}"
    "--out_exon {output.exon} --out_intron {output.intron} --geneRange True"


  rule bedtools_subtract:
    input:
      exon="output/gencode_v38_exon.bed"
      generange="output/geneRange.bed"
    output:
      "output/gencode_v38.intron_nr.bed"
    shell:
      "bedtools substract -a {input.generange} -b {input.exon} > {output}"

  rule count_intronic_reads:
    input:
      bam="bamdir/{sample}.sorted.uniq.bam"
      bed="output/gencode_v38.intron_nr.bed"
    output:
      "output/{sample}.stat.bed"

    shell:
      "bedtools multicov -bams {input.bam} -bed {input.bed} > {output}"
