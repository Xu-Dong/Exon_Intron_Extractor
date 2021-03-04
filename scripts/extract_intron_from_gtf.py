#!~/tools/anaconda2/bin/python
'''
Extract intron from given gtf file, and generate bed files
Usage: python extract_intron_from_gtf.py --gtf <gtf> --out <bed>
Code by: Xudong Zou, 2021-02-20
'''
import argparse
import re

# Function --------------------------------
def extract_exon(gtf_file):
	keep_chr = []
	for i in range(22):
		keep_chr.append('chr'+str(i+1))
	keep_chr = keep_chr + ['chrX','chrY']
	with open(gtf_file,'r') as fh:
		transcript_exon = {}
		geneid,transcript_id = '',''
		for line in fh.readlines():
			line = line.strip()
			w = line.split("\t")
			chrn = w[0]
			strand = w[6]
			entry_type = w[2]
			geneid_patt = re.search(r'gene_id\s"(\w+)";',w[8])
			transcript_patt = re.search(r'transcript_id\s"(\w+)";',w[8])
			if geneid_patt:
				gene_id = geneid_patt.group(1)
			else:
				gene_id = "NA"
			if transcript_patt:
				transcript_id = transcript_patt.group(1)
				transcript_id = chrn+":"+transcript_id+":"+gene_id+":"+strand
				if entry_type == "exon" and chrn in keep_chr:
					exon = (int(w[3]),int(w[4]))
					if transcript_id not in transcript_exon:
						transcript_exon[transcript_id] = [exon]
					else:
						transcript_exon[transcript_id].append(exon)
				else:
					continue
			else:
				continue
	return transcript_exon


def extract_intron(exon_list):
	intron_list = []
	for i in range(len(exon_list)-1):
		intron = (exon_list[i][1],exon_list[i+1][0])
		intron_list.append(intron)
	return intron_list

# Main -----------------------------------

parser = argparse.ArgumentParser(description='')
parser.add_argument('--gtf',help="specify a gtf file")
parser.add_argument('--out',help="specify a filename for output")

args = parser.parse_args()

exon_dict = extract_exon(args.gtf)

fho = open(args.out,'w')
for t in exon_dict:
	chrname,tid,gid,strand = t.split(":")
	if len(exon_dict[t]) > 1:
		introns = extract_intron(exon_dict[t])
		for intron in introns:
			print >>fho,"%s\t%d\t%d\t%s\t%d\t%s" % (chrname,intron[0]-1,intron[1],gid+":"+tid,intron[1]-intron[0]+1,strand)

			
fho.close()
print "Done!"
print "Generate intron bed in file:%s" % (args.out)
print "@ZouXD,2021-02-22"
