import os
import sys
import ete3

def get_node2present(treefile):

    with open(treefile) as f:
        tree = ete3.Tree(f.readline(),format=1)

    node2present = dict()
    for n in tree.traverse("postorder"):
        if n.name == "":
            continue
        n.add_feature("dist_to_present", 0)
        if not n.is_leaf():
            c1, _ = n.get_children()
            n.dist_to_present = c1.dist_to_present + c1.dist                
            node2present[n.name] = n.dist_to_present

    for k,v in node2present.items():
        print("\t".join((k,str(v))))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print ("usage: python get_node2present.py tree")
        exit(0)

    _, treefile  = sys.argv
    get_node2present(treefile)
