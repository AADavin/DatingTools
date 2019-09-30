import sys

def filter_constraints(constraintfile, cutoff):

    with open(constraintfile) as f:
        for line in f:
            fam, donor, recipient, wt = line.strip().split("\t")
            if float(wt) >= cutoff:
                new_line = "\t".join([fam, donor, recipient, wt])
                print(new_line)

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("usage: python filter_constraints.py AllConstraints 0.05")
        exit(0)
    scr, constraintfile, cutoff = sys.argv
    filter_constraints(constraintfile, float(cutoff))
