import os
import sys
import ete3

def get_patchiness(reftree, mytree):

    with open(reftree) as f:
        reftree = ete3.Tree(f.readline(), format=1)
    with open(mytree) as f:
        mytree = ete3.Tree(f.readline(), format=1)
        
    msps = {l.name for l in mytree.get_leaves()}
    for n in reftree.traverse("postorder"):
        n.add_feature("sps", {l.name for l in n.get_leaves()})
        if msps <= n.sps:
            print(len(msps) / float(len(n)))
            break

        



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python get_patchiness speciestree marker")
        exit(0)

    _, reftree, yourtree  = sys.argv
    get_patchiness(reftree, yourtree)
