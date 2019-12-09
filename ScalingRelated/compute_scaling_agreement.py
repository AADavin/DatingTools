import os
import sys
import numpy as np
import ete3

def get_node2present(treefile):

    with open(treefile) as f:
        tree = ete3.Tree(f.readline(),format=1)

    node2present = dict()
    for n in tree.traverse("postorder"):
        n.add_feature("dist_to_present", 0)
        if not n.is_leaf():
            c1, _ = n.get_children()
            n.dist_to_present = c1.dist_to_present + c1.dist
            node2present[n.name] = n.dist_to_present
    return node2present


def compute_scaling_agreement(reftree, redtree):
    
    x = list()
    y = list()

    n2present_s = get_node2present(redtree)
    n2present_ref = get_node2present(reftree)

    node_order = sorted(n2present_s.items(), key=lambda x: x[1])
    node_order = [x[0] for x in node_order][::-1]
    mnode_order = list()
    
    for n in node_order:    
        if n == "Root":
            continue
        if n not in n2present_s or n not in n2present_ref:
            continue
        t1 = n2present_ref[n]
        t2 = n2present_s[n]
        x.append(t1)
        y.append(t2)    
        mnode_order.append(n)
    

    # We inverse the distance (easier to read), by substractint 1-d


    x = np.array(x)
    y = np.array(y)
    print("\t".join(["REF_VALUE","RED_VALUE","NODE"]))
    for v1, v2, v3 in zip(x,y,mnode_order):
        print("\t".join((str(v1),str(v2),v3)))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python compute_scaling_agreement.py reftree redtree")
        exit(0)

    _, reftree, redtree  = sys.argv
    compute_scaling_agreement(reftree, redtree)
