import sys
import os
import ete3

def compute_reds(tree_file):


    with open(tree_file) as f:
        for l in f:
            mtree = ete3.Tree(l.strip(), format=1)
            for n in mtree.traverse():
                if n.is_root():
                    n.add_feature("RED", 0.0)
                    continue
                if n.is_leaf():
                    n.add_feature("RED", 1)
                    continue

                n.add_feature("RED", 0.0)

                u = get_average(n)
                n.RED = n.up.RED + ((n.dist / u) * (1 - n.up.RED))

            for n in mtree.traverse():
                if n.is_root():
                    continue
                n.dist = n.RED - n.up.RED

            print(mtree.write(format=1))


def get_average(node):

    dists = list()

    for l in node.get_leaves():
        mdist = l.get_distance(node.up)
        dists.append(mdist)

    return(float(sum(dists))/len(dists))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python compute_reds tree_file")
        exit(0)

    scr, tree_file = sys.argv
    compute_reds(tree_file)
