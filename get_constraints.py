import sys
import ete3

def get_constraints(treefile, transfersfile):

    myparents = dict()
    leaves = set()
    with open(treefile) as f:
     
        mytree = ete3.Tree(f.readline().strip(), format=1)

    for node in mytree.traverse():
        if node.is_root():
            myparents[node.name] = "Root"
        else:
            if node.is_leaf():
                leaves.add(node.name)
            myparents[node.name] = node.up.name

    with open(transfersfile) as f:
        for line in f:
            donor, recipient, wt = line.strip().split("\t")
            if recipient in leaves:
                continue
            new_line = "\t".join([myparents[donor], recipient, wt])
            print(new_line)



if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print ("usage: python get_constraints.py RefTree transfersfile")
        exit(0)

    scr,treefile,transferfile = sys.argv

    get_constraints(treefile, transferfile)
