import sys
import os


def read_bootstrap(keyword):

    replicate_files = [x for x in os.listdir("./") if "partial_order" in x and keyword in x]
    number_files = len(replicate_files)
    constraints = dict()
    for replicate_file in replicate_files:
        with open("./" + replicate_file) as f:
            for line in f:
                dn, rc, wt, dir = line.strip().split(" ")
                if dn not in constraints:
                    constraints[dn] = dict()
                if rc not in constraints[dn]:
                    constraints[dn][rc] = {"n":0, "wt": 0.0}
                constraints[dn][rc]["n"] += 1
                constraints[dn][rc]["wt"] += float(wt)

    for dn in constraints:
        for rc in constraints[dn]:
            line = "\t".join([dn, rc, str(constraints[dn][rc]["n"]), str(constraints[dn][rc]["wt"] / constraints[dn][rc]["n"])])
            print(line)



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python read_boostrap.py keyword")
        exit(0)

    scr, keyword = sys.argv
    read_bootstrap(keyword)
