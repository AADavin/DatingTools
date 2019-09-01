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
            dn, rc, wt = l.strip().split("\t")
            if dn not in constraints:
                constraints[dn] = dict()
            if rc not in constraints[dn][rc]:
                constraints[dn][rc] = 0.0
            constraints[dn][rc] += float(wt)
    return constraints

def read_calibrations(calibrations_file):
    '''

    :param calibrations_file: A fossil calibration file, PhyloBayes format
    :return: A list of tuples containing node1, node2, maximim_age, minimum_age
    '''
    calibrations = list()
    with open(calibrations_file) as f:
        f.readline()
        for l in f:
            n1, n2, mxc, mc = l.strip().split("\t")
            calibrations.append((n1,n2,float(mxc),float(mc)))
    return calibrations


def propagate_constraints(mtree, constraints, calibrations):
    '''

    Propagates fossil-based calibrations using transfer-based constraints

    :param mtree: A ete3.Tree (use read_tree())
    :param constraints: A dict of constraints (use read_constraints())
    :param calibrations: A list of calibrations (use read_calibrations())
    :return: A newick tree with propagatepropagate_constraints.py:56d constraints
    '''

    pass











if __name__ == "__main__":

    args =  sys.argv

    if len(args) != 4:
        print("Usage: python propagate_constraints.py species_tree constraints_file calibrations_file")

    else:

        _, species_tree, constraints_file, calibrations_file

        mtree = read_tree(species_tree)
        constraints = read_constraints(constraints_file)
        calibrations = read_calibrations(calibrations_file)

        propagate_constraints(mtree, constraints, calibrations)
