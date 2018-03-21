import sys

def compute_conflict(node_order, constraints):

    conflict = float()
    ranking = {node:rank for rank,node in enumerate(node_order)}
    for dn,rcs in constraints.iteritems():
        for rc,wt in rcs.iteritems():
            if ranking[dn] > ranking[rc]:
                conflict += wt
    return conflict

def get_constraints(constraints_file):

    constraints = dict()
    total_w = float()

    with open(constraints_file) as f:

        for line in f:

            dn,rc,wt = line.strip().split("\t")

            if dn not in constraints:
                constraints[dn] = dict()

            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0

            constraints[dn][rc] += float(wt)
            total_w += float(wt)

    return (constraints, total_w)

def get_conflict(order_file, constraints_file):

    constraints = get_constraints(constraints_file)

    with open(order_file) as f:
        for line in f:
            myorder = line.strip().split(",")
            print compute_conflict(myorder,constraints)



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python get_conflict.py order constraints")
        exit(0)

    scr, order_file, constraints_file = sys.argv
    compute_conflict(order_file, constraints_file)