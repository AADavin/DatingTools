import ete3
import sys
import os

def prepare_singletons_tree(tree_file, rec_folder):

    rec_files = [x for x in os.listdir(rec_folder) if x.endswith(".uml_rec")]

    with open(tree_file) as f:
        reftree = ete3.Tree(f.readline().strip(),format=1)

    branch2singl = dict()
    for rec_file in rec_files:
        with open(os.path.join(rec_folder, rec_file)) as f:
            found = False
            for l in f:
                if found == True:
                    h = l.strip().split("\t")
                    singl = float(h[-2])
                    branch = h[1]
                    if "(" in branch:
                        branch = branch.split("(")[0]
                    if branch not in branch2singl:
                        branch2singl[branch] = 0.0
                    branch2singl[branch] += singl
                if "singletons" in l:
                    found = True

    for n in reftree.traverse():
        if n.is_leaf():
            n.dist = branch2singl[n.name.split(":")[0]]
        else:
            if n.name not in branch2singl:
                continue
            n.dist = branch2singl[n.name]

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python prepare_singletons_tree.py tree_file rec_folder")
        exit(0)

    scr, tree_file, rec_folder  = sys.argv
    prepare_singletons_tree(tree_file, rec_folder)
