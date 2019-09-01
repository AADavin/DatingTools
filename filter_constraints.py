import sys
import ete3



def filter_constraints(*args):

    input_files = args[0]

    constraints_infile = input_files[0]
    node1 = input_files[1]
    node2 = input_files[2]
    treefile = input_files[3]

    with open(treefile) as f:
        mtree = ete3.Tree(f.readline().strip(), format=1)

    mnode1 = mtree&node1
    mnode2 = mtree&node2
    dnode1 = {x.name for x in mnode1.traverse()}
    dnode2 = {x.name for x in mnode2.traverse()}

    with open(constraints_infile) as f:
        for line in f:
            dn, rc, js, wt = line.strip().split("\t")
            if (dn in dnode1 and rc in dnode2) or (dn in dnode2 and rc in dnode1):
                print(line.strip())




if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("usage: python filter_constraints.py constraints_dataframe node1 node2 treefile")
        exit(0)

    filter_constraints(sys.argv[1:])