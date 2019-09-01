import ete3
import sys

def mapper(mytree, cmn_ancestors):

    mytree = ete3.Tree(mytree,format=1)

    for k,v in cmn_ancestors.items():

        mynode = mytree.get_common_ancestor(v[0],v[1])
        mynode.name = k

    return mytree.write(format=1, format_root_node=True)


def map_trees(reftree_file,mytree_file):

    with open(reftree_file) as f:

        reftree = ete3.Tree(f.readline().strip(),format=1)

    mynodes = [node.name for node in reftree.traverse()]
    cmn_ancestors = dict()
    for n in mynodes:
        for m in mynodes:
            ancestor = reftree.get_common_ancestor(n,m)
            cmn_ancestors[ancestor.name] = (m,n)

    with open(mytree_file) as f:
        for tree in f:
            print(mapper(tree.strip(),cmn_ancestors))



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python map_trees.py reftree trees")
        exit(0)

    scr, reftree_file, tree_file  = sys.argv
    map_trees(reftree_file, tree_file)