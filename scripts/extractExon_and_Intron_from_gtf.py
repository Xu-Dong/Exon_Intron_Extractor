#!~/tools/anaconda2/bin/python

'''
Extract exons and introns from given gtf file, and generate bed files
Code by: Xudong Zou
Start time: 2021-02-20
LastModified time: 2021-06-15
'''

import argparse
import re

# Function --------------------------------
def extract_exon(gtf_file,skip_rows):
	keep_chr = []
	for i in range(22):
		keep_chr.append('chr'+str(i+1))
	keep_chr = keep_chr + ['chrX','chrY']
	with open(gtf_file,'r') as fh:
		transcript_exon = {}
		geneid,transcript_id,genename,genetype = '','','',''
		for line in fh.readlines()[skip_rows:]:
			line = line.strip()
			w = line.split("\t")
			chrn = w[0]
			strand = w[6]
			entry_type = w[2]	
			# build match patterns
			geneid_patt_1 = re.search(r'gene_id\s"(\w+)";',w[8])
			geneid_patt_2 = re.search(r'gene_id\s"(\w+\.\d+)";',w[8])# with version number
			transcript_patt_1 = re.search(r'transcript_id\s"(\w+)";',w[8])
			transcript_patt_2 = re.search(r'transcript_id\s"(\w+\.\d+)";',w[8])#with version number
			genename_patt = re.search(r'gene_name\s"(.*?)";',w[8])
			genetype_patt = re.search(r'gene_type\s"(.*?)";',w[8])
			if geneid_patt_1:
				gene_id = geneid_patt_1.group(1)
			elif geneid_patt_2:
				gene_id = geneid_patt_2.group(1)
			else:
				gene_id = "NA"
			if genename_patt:
				genename = genename_patt.group(1)
			else:
				genename = "NA"
			if genetype_patt:
				genetype = genetype_patt.group(1)
			else:
				genetype = "NA"
			if transcript_patt_1 or transcript_patt_2:
				transcript_id = transcript_patt_1.group(1) if transcript_patt_1 else transcript_patt_2.group(1)
				transcript_id = chrn+":"+transcript_id+":"+gene_id+":"+strand+":"+genename+":"+genetype
				if entry_type == "exon" and chrn in keep_chr:
					exon = (int(w[3]),int(w[4])) #1-based coordinate
					if transcript_id not in transcript_exon:
						transcript_exon[transcript_id] = [exon]
					else:
						transcript_exon[transcript_id].append(exon)
				else:
					continue
			else:
				continue
	return transcript_exon

# get the intron(s) from a exon list in a transcript
def extract_intron(exon_list):
	intron_list = []
	for i in range(len(exon_list)-1):
		intron = (exon_list[i][1]+1,exon_list[i+1][0]-1) # 1-based coordinate with both ends included
		intron_list.append(intron)
	return intron_list

# get the range of a gene, input a gtf file and output a dict: {gene:(chr,start,end,strand,genetype)}
def extract_gene_range(gtf_file,skip_rows):
	keep_chr = []
	for i in range(22):
		keep_chr.append('chr'+str(i+1))
	keep_chr = keep_chr + ['chrX','chrY']
	with open(gtf_file,'r') as fh:
		gene_range = {}
		geneid,genename,genetype = '','',''
		for line in fh.readlines()[skip_rows:]:
			line = line.strip()
			w = line.split("\t")
			chrn = w[0]
			strand = w[6]
			entry_type = w[2]
			gene_start = w[3]
			gene_end = w[4]
			# build match patterns
			geneid_patt_1 = re.search(r'gene_id\s"(\w+)";',w[8])
			geneid_patt_2 = re.search(r'gene_id\s"(\w+\.\d+)";',w[8])# with version number
			genename_patt = re.search(r'gene_name\s"(.*?)";',w[8])
			genetype_patt = re.search(r'gene_type\s"(.*?)";',w[8])
			if geneid_patt_1:
				geneid = geneid_patt_1.group(1)
			elif geneid_patt_2:
				geneid = geneid_patt_2.group(1)
			else:
				geneid = "NA"
			if genename_patt:
				genename = genename_patt.group(1)
			else:
				genename = "NA"
			if genetype_patt:
				genetype = genetype_patt.group(1)
			else:
				genetype = "NA"
			if w[2]=="gene" and chrn in keep_chr:
				gene_range[geneid] = (chrn,gene_start,gene_end,strand,genetype) # 1-based coordinates and with both ends included
			else:
				continue
	return gene_range


# Main -----------------------------------

# define args 
parser = argparse.ArgumentParser(description='')
parser.add_argument('--gtf',help="specify a gtf file")
parser.add_argument('--out_exon',help="specify a filename for exon output")
parser.add_argument('--out_intron',help="specify a filename for intron output")
parser.add_argument('--geneRange', default=True,action="store_true",help="if True, output gene range into a bed file: geneRange.bed")

# interpret args
args = parser.parse_args()

# extract exon for each transcript
exon_dict = extract_exon(args.gtf,5) # remove 5 header rows

# print out exons in bed format
fho = open(args.out_exon,'w')
for t in exon_dict:
	chrname,tid,gid,strand,gname,gtype = t.split(":")
	for exon in exon_dict[t]:
		print >>fho, "%s\t%d\t%d\t%s\t%s\t%s\t%s\t%s" % (chrname,exon[0]-1,exon[1],gid+":"+tid,exon[1]-exon[0]+1,strand,gname,gtype)
fho.close()

# extract and output introns dependent on exon structures
fho = open(args.out_intron,'w')
for t in exon_dict:
	chrname,tid,gid,strand,gname,gtype = t.split(":")
	if len(exon_dict[t]) > 1:
		sorted_exons = sorted(exon_dict[t],key=lambda x:x[0])
		introns = extract_intron(sorted_exons)
		for intron in introns:
			print >>fho,"%s\t%d\t%d\t%s\t%d\t%s\t%s\t%s" % (chrname,intron[0]-1,intron[1],gid+":"+tid,intron[1]-intron[0]+1,strand,gname,gtype)

			
fho.close()

# gene range
if args.geneRange:
	gene_range = extract_gene_range(args.gtf,5) # geneid:(chrn,gene_start,gene_end,strand,genetype)
	fho = open("geneRange.bed",'w')
	for gene in gene_range:
		chrN = gene_range[gene][0]
		startP = int(gene_range[gene][1])
		endP = int(gene_range[gene][2])
		strand = gene_range[gene][3]
		genetype = gene_range[gene][4]
		print >> fho, "%s\t%d\t%d\t%s\t%d\t%s" % (chrN,startP-1,endP,gene,endP-startP+1,strand)
	fho.close()

print "Done!"
print "Generate exon bed in file:%s" % (args.out_exon)
print "Generate intron bed in file:%s" % (args.out_intron)
print "Defaulty there should also have one file namely geneRange.bed containing gene ranges"
