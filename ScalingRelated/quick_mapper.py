import os
import sys
import ete3

def quick_mapper(reftree, mytree):

    with open(reftree) as f:
        reftree = ete3.Tree(f.readline(), format=1)
    with open(mytree) as f:
        mytree = ete3.Tree(f.readline(), format=1)


    refnodes = [node for node in reftree.traverse() if not node.is_leaf()]
    for i,n in enumerate(refnodes):
        c1,c2 = n.get_children()
        c1l = c1.get_leaves()[0].name
        c2l = c2.get_leaves()[0].name        
        n1 = mytree&c1l
        n2 = mytree&c2l        
        try: 
            mn = mytree.get_common_ancestor(c1l, c2l)
            mn.name = n.name
        except:
            print("Couldn't map node %s" % n.name)
    print(mytree.write(format=1))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python quick_mapper.py reftree yourtree")
        exit(0)

    _, reftree, yourtree  = sys.argv
    quick_mapper(reftree, yourtree)
