import sys

def get_constraints(constraints_file):
    constraints = dict()
    total_w = float()

    with open(constraints_file) as f:

        for line in f:

            dn, rc, wt = line.strip().split("\t")

            if dn not in constraints:
                constraints[dn] = dict()

            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0

            constraints[dn][rc] += float(wt)
            total_w += float(wt)

    return (constraints, total_w)


def get_constraints_for_order(orderfile, constraintsfile):

    with open(orderfile) as f:
        order = f.readline().strip().split(",")

    ranking = {node: rank for rank, node in enumerate(order)}

    constraints, total_w = get_constraints(constraintsfile)

    for dn, rcs in constraints.items():
        for rc, wt in rcs.iteritems():
            if ranking[dn] > ranking[rc]:
                print("\t".join(dn,rc, str(wt)))



if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print("usage: python get_constraints_for_order.py orderfile constraints")
        exit(0)

    scr, orderfile, constraints = sys.argv

    get_constraints_for_order(orderfile, constraints)

