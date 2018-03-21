import sys
from ete3 import PhyloTree

def prepare_constraints(input_transfers,mytree,output_constraints,col_donor,col_acceptor,col_wt):

    myparents = dict()
    with open(mytree) as f:
        mytree = PhyloTree(f.next().strip(),format=1)
    for node in mytree.traverse():
        if node.is_root():
            myparents[node.name] = "Root"
        else:
            myparents[node.name] = node.up.name

    clean_constraints = dict()

    with open(input_transfers) as f:

        for line in f:
            handle = line.strip().split("\t")
            acceptor = handle[col_acceptor]
            donor_t = handle[col_donor]
            wt = handle[col_wt]

            try:

                b = int(acceptor)

            except:

                continue
                # In this case the acceptor is a leaf and for that, that is not informative. We get rid of it

            donor_c = myparents[donor_t]

            if donor_c == acceptor:
                continue
            if donor_c == "Root":
                continue

            if donor_c not in clean_constraints:
                clean_constraints[donor_c] = dict()
            if acceptor not in clean_constraints[donor_c]:
                clean_constraints[donor_c][acceptor] = float()

            clean_constraints[donor_c][acceptor] += float(wt)

    with open(output_constraints,"w") as f:
        for dn, rcs in clean_constraints.iteritems():
            for rc, wt in rcs.iteritems():
                myline = "\t".join([dn,rc,str(wt)])+"\n"
                f.write(myline)

if __name__ == "__main__":

    if (len(sys.argv) != 7):
        print ("usage: python prepare_constraints.py input_transfers species_tree output_constraints col_donor col_acceptor col_weight")
        exit(0)

    scr,input_transfers,mytree,output_constraints,col_donor,col_acceptor, col_weight = sys.argv

    prepare_constraints(input_transfers,mytree,output_constraints,int(col_donor),int(col_acceptor),int(col_weight))
