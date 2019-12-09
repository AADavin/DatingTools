import os
import sys

_, extension = sys.argv

files = [x for x in os.listdir("./") if x.endswith(extension)]

def fasta_parser(myfile):
    with open(myfile) as f:

        header = ""
        seq = ""
        for line in f:
            if line[0] == ">":
                if seq != "":
                    yield (header[1:], seq)
                    header = line.strip()
                    seq = ""
                else:
                    header = line.strip()
            else:
                seq += line.strip()
        yield (header[1:], seq)



fam2sps = dict()
fam2length = dict()
allsps = set()
sp2con= dict()
for mfile in files:
    fam2sps[mfile] = set()
    for h, seq in fasta_parser(mfile):
        fam2sps[mfile].add(h)
        allsps.add(h)
    fam2length[mfile]= len(seq)

for sp in allsps:
    sp2con[sp] = ""

for fam, sps in fam2sps.items():

    sp2seq = dict()

    for h,seq in fasta_parser(fam):
        sp2seq[h] = seq

    for sp in allsps:
        if sp in sp2seq:
            sp2con[sp] += sp2seq[sp]
        else:
            sp2con[sp] += "-" * fam2length[fam]

for k, v in sp2con.items():
    print(">" + k)
    #print(v)



