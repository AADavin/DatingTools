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

def cut_down_trees(mtree, n):
    '''

    Propagates fossil-based calibrations using transfer-based constraints

    :param mtree: A ete3.Tree (use read_tree())
    :param constraints: A dict of constraints (use read_constraints())
    :param calibrations: A list of calibrations (use read_calibrations())
    :return: Creates three files. 1- Tree with Fossil calibrations. 2- Tree with Fossil calibrations propagated 3-Nodes with changes between 1 and 2
    '''

if __name__ == "__main__":

    args =  sys.argv

    if len(args) != 3:
        print("Usage: python cut_down_trees.py species_tree number_of_smaller_trees")

    else:

        _, species_tree, n, = sys.argv

        mtree = read_tree(species_tree)
        cut_down_trees(mtree, int(n))
