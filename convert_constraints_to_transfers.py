import sys
import ete3

def convert_constraints_to_transfers(constraints_file, transfers_file, tree_file, include_leaves):

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
            try:
                 dn, rc, wt, _ = line.strip().split(" ")
            except:
                 dn, rc, wt = line.strip().split("\t")
            if dn not in constraints:
                constraints[dn] = dict()
            if rc not in constraints[dn]:
                constraints[dn][rc] = 0
    with open(transfers_file) as f:
        for line in f:
            fam, dn, rc, wt = line.strip().split("\t")
            if "(" in dn:
                dn = dn.split("(")[0]
            if "(" in rc:
                rc = rc.split("(")[0]
            if node2parent[dn] == "None":
                continue
            if include_leaves == False and rc in leaves:
                continue 
            if include_leaves == True and rc in leaves:
                if fam not in saved_transfers:
                    saved_transfers[fam] = dict()
                if dn not in saved_transfers[fam]:
                    saved_transfers[fam][dn] = dict()
                if rc not in saved_transfers[fam][dn]: 
                    saved_transfers[fam][dn][rc] = 0
                                   
                saved_transfers[fam][dn][rc] += float(wt)
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
                mline = "\t".join([fam, dn, dn_c, rc, wt])
                print(mline)


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("usage: python convert_constraints_to_transfers constraints_file transfer_file tree_file False")
        exit(0)

    scr, constraints_file, transfers_file, tree_file, leaves = sys.argv
    convert_constraints_to_transfers(constraints_file, transfers_file, tree_file, bool(leaves))
