import os
import sys
import ete3

def read_tree(tree_file):
    '''
    :param tree_file: A file containing a newick tree
    :return: A ete3.Tree object
    '''

    with open(tree_file) as f:
        mtree = ete3.Tree(f.readline().strip(),format=1)
    return(mtree)

def read_constraints(constraints_file):
    '''

    :param constraints_file: A .tsv file contaning Donor, Recipient and Weight
    :return: A dict of constraints
    '''
    constraints = dict()
    with open(constraints_file) as f:
        for l in f:
            try:
                dn, rc, wt = l.strip().split("\t")
            except:
                _, dn, rc, wt = l.strip().split("\t")
            if dn not in constraints:
                constraints[dn] = dict()
            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0
            constraints[dn][rc] += float(wt)
    return constraints

def read_calibrations(calibrations_file):
    '''

    :param calibrations_file: A fossil calibration file, PhyloBayes format
    :return: A list of tuples containing node1, node2, upper_age, lower_age
    '''
    calibrations = list()
    with open(calibrations_file) as f:
        f.readline()
        for l in f:
            n1, n2, upper, lower = l.strip().split("\t")
            calibrations.append((n1,n2,float(upper),float(lower)))
    return calibrations


def propagate_upwards(mtree):

    upper = 1000000000

    for l in mtree.get_leaves():
        for n in l.get_ancestors():
            if n.upper > upper:
                n.upper = upper



def propagate_downwards():
    pass

def propagate_horizontally():
    pass


def propagate_constraints(mtree, constraints, calibrations):
    '''

    Propagates fossil-based calibrations using transfer-based constraints

    :param mtree: A ete3.Tree (use read_tree())
    :param constraints: A dict of constraints (use read_constraints())
    :param calibrations: A list of calibrations (use read_calibrations())
    :return: Creates three files. 1- Tree with Fossil calibrations. 2- Tree with Fossil calibrations propagated 3-Nodes with changes between 1 and 2
    '''


    # We start by assigning each inner node of the species tree two new features

    for n in mtree.traverse():
        if not n.is_leaf():
            n.add_feature("upper", 10000000000000) # Arbitrarily big number
            n.add_feature("lower", 0)


    # Then, for each calibration, we assign the calibration and propagate the constraint

    for calibration in calibrations:
        n1, n2, upper, lower = calibration


        # First, we propagate the upper constraint downwards the tree

        mn1 = mtree&n1
        mn2 = mtree&n2

        mnode = mtree.get_common_ancestor(mn1, mn2)

        if upper != -1.0 : # We check that the limit exists!
            for n in mnode.traverse():
                if not n.is_leaf():
                    if n.upper > upper:
                        n.upper = upper

        # Second we propagate the lower constraint upwards the tree

        if lower != -1.0:

            if mnode.lower < lower:
                mnode.lower = lower

            for n in mnode.get_ancestors():
                if n.lower < lower:
                    n.lower = lower

    # We create a file with the constraints of each node:
    fossil2limit = dict()
    with open("./FossilLimits.tsv", "w") as f:
        for n in mtree.traverse():
            if not n.is_leaf():
                if n.lower == 0.0:
                    mlower = "-1"
                else:
                    mlower = str(n.lower)
                line = "\t".join([n.name, str(n.upper), str(mlower)]) + "\n"
                fossil2limit[n.name] = (str(n.upper), str(mlower))
                f.write(line)


    # Now we have propagated all the calibrations upwards and downwards.
    # It is time to use the transfers to propagate the constrains horizontally

    # We might need to to it several times

    changes = True

    while(changes):

        count_changes = 0

        for dn, rcs in constraints.items():
            for rc, wt in rcs.items():

                dn_node = mtree&dn
                rc_node = mtree&rc

                if dn_node.lower < rc_node.lower:

                    count_changes +=1

                    dn_node.lower = rc_node.lower

                    # We propagate upwards

                    for n in dn_node.get_ancestors():
                        if n.lower < dn_node.lower:
                            n.lower = dn_node.lower

                if dn_node.upper < rc_node.upper:

                    count_changes += 1

                    rc_node.upper = dn_node.upper

                    # We propagate downwards

                    for n in rc_node.traverse():
                        if not n.is_leaf():
                            if n.upper > rc_node.upper:
                                n.upper = rc_node.upper
        if count_changes == 0:
            changes = False

    #  The constraints has been fully propagated
    transfer2limit = dict()
    with open("./FossilAndTransferLimits.tsv", "w") as f:
        for n in mtree.traverse():
            if not n.is_leaf():
                if n.lower == 0.0:
                    mlower = "-1"
                else:
                    mlower = str(n.lower)
                line = "\t".join([n.name, str(n.upper), str(mlower)]) + "\n"
                transfer2limit[n.name] = (str(n.upper), str(mlower))
                f.write(line)

    # Now we print the differences:

    with open("DiffTransferFossil", "w") as f:
        for n in fossil2limit:
            if fossil2limit[n] != transfer2limit[n]:
                f.write("\t".join([n, transfer2limit[n][0], transfer2limit[n][1]]) + "\n")


if __name__ == "__main__":

    args =  sys.argv

    if len(args) != 4:
        print("Usage: python propagate_constraints.py species_tree constraints_file calibrations_file")


    else:

        _, species_tree, constraints_file, calibrations_file = sys.argv

        mtree = read_tree(species_tree)
        constraints = read_constraints(constraints_file)
        calibrations = read_calibrations(calibrations_file)

        propagate_constraints(mtree, constraints, calibrations)
