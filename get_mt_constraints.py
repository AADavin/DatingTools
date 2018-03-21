from ete3 import PhyloTree
import sys

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

def filter_constraints(constraints_file, tree_file):

    mt_order = get_node_order(tree_file)

    constraints, total_w = get_constraints(constraints_file)

    new_total_w = 0

    new_constraints = dict()

    for dnr, rcpts in constraints.iteritems():

        for rc, wt in rcpts.iteritems():

            if mt_order.index(dnr) < mt_order.index(rc):

                if dnr not in new_constraints:

                    new_constraints[dnr] = dict()

                if rc not in new_constraints[dnr].iteritems():

                    new_constraints[dnr][rc] = float()

                new_constraints[dnr][rc] = wt
                new_total_w += wt

    return (new_constraints, new_total_w)

def get_node_order(tree_file):

    with open(tree_file) as f:
        mytree = PhyloTree(f.next().strip(),format=1)

    distances = dict()

    for mynode in mytree.traverse():

       if mynode.is_leaf():
           continue

       one_leaf = mynode.get_leaves()[0]
       dist = mynode.get_distance(one_leaf)
       distances[mynode.name] = dist

    node_order = sorted(distances.items(), key=lambda x: x[1])
    node_order =  [x[0] for x in node_order][::-1]

    return node_order


def get_mt_constraints(tree_file, constraints_infile, constraints_outfile):

    constraints, total_weight = filter_constraints( constraints_infile, tree_file)

    with open(constraints_outfile, "w") as f:
        for dnr, rcpts in constraints.iteritems():
            for rct,wt in rcpts.iteritems():
                line = "\t".join([dnr ,rct ,str(wt)]) + "\n"
                f.write(line)



if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print ("usage: python get_mt_constraints.py species_tree constraints_infile constraints_outfile")
        exit(0)
    scr, tree_file, constraints_infile, constraints_outfile = sys.argv
    get_mt_constraints(tree_file, constraints_infile, constraints_outfile)