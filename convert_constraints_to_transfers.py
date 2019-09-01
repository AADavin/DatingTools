import sys
import os
import ete3

def convert_constraints_to_transfers(constraints_file, transfers_file, tree_file):

    with open(tree_file) as f:
        mtree = ete3.Tree(f.readline().strip(),format=1)

    node2parent = dict()
    leaves = set()
    constraints = dict()

    saved_transfers = dict()

    for n in mtree.traverse():
        if n.is_root():
            node2parent[n.name] = "None"
        else:
            node2parent[n.name] = n.up.name

        if n.is_leaf():
            leaves.add(n.name)

    with open(constraints_file) as f:
        for line in f:
            dn, rc, js, wt = line.strip().split("\t")
            if int(js) < 95:
                continue
            if dn not in constraints:
                constraints[dn] = dict()
            if rc not in constraints[dn]:
                constraints[dn][rc] = 0

    with open(transfers_file) as f:

        for line in f:
            fam, dn, rc, wt = line.strip().split("\t")
            if node2parent[dn] == "None":
                continue
            if rc in leaves:
                continue
            dn_c = node2parent[dn]

            if dn_c in constraints:
                if rc in constraints[dn_c]:
                    if fam not in saved_transfers:
                        saved_transfers[fam] = dict()
                    if dn not in saved_transfers[fam]:
                        saved_transfers[fam][dn] = dict()
                    if rc not in saved_transfers[fam][dn]:
                        saved_transfers[fam][dn][rc] = 0.0
                    saved_transfers[fam][dn][rc] += float(wt)


    for fam in saved_transfers:
        for dn in saved_transfers[fam]:
            for rc in saved_transfers[fam][dn]:
                wt = str(saved_transfers[fam][dn][rc])
                dn_c = node2parent[dn]
                mline = "\t".join([fam, dn, rc, dn_c, wt])
                print(mline)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("usage: python convert_constraints_to_transfers ftransfer_file tree_file")
        exit(0)

    scr, constraints_file, transfers_file, tree_file = sys.argv
    convert_constraints_to_transfers(constraints_file, transfers_file, tree_file)
