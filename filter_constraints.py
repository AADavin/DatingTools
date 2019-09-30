import sys

def filter_transfers(transferfile, cutoff):

    with open(transferfile) as f:
        for line in f:
            fam, donor, recipient, wt = line.strip().split("\t")
            if float(wt) >= cutoff:
                new_line = "\t".join([fam, donor, recipient, wt])
                print(new_line)

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("usage: python filter_transfers.py AllTransfers.tsv 0.05")
        exit(0)
    scr, transferfile, cutoff = sys.argv
    filter_transfers(transferfile, float(cutoff))
