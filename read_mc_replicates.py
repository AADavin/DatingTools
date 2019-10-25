import sys
import os

def read_mc_replicates():

    replicate_constraints = [x for x in os.listdir("./") if x.endswith("rconstraints")]

    number_files = len(replicate_constraints)
    constraints = dict()

    for replicate_file in replicate_constraints:
        with open(replicate_file) as f:
            for line in f:
                dn, rc, wt  = line.strip().split("\t")
                if dn not in constraints:
                    constraints[dn] = dict()
                if rc not in constraints[dn]:
                    constraints[dn][rc] = {"n":0, "wt": 0.0}
                constraints[dn][rc]["n"] += 1
                constraints[dn][rc]["wt"] += float(wt)

    for dn in constraints:
        for rc in constraints[dn]:
            line = "\t".join([dn, rc, str(constraints[dn][rc]["n"]), str(constraints[dn][rc]["wt"] / number_files)])
            print(line)


if __name__ == "__main__":

    if len(sys.argv) != 1:
        print("usage: python read_mc_replicates.py")
        exit(0)

    scr = sys.argv
    read_mc_replicates()
