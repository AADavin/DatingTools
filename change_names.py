import ete3
import itertools
import os


mypath = "/Users/adriandavin/Desktop/Bioinformatics/SimuLyon/ExampleMaxTiC/Test1/G/Gene_trees"
mytree = ete3.Tree("(((((n53:0.930813,n54:0.930813)n45:3.13103,n46:4.06184)n40:24.186,(n23:19.032,(n47:3.54213,n48:3.54213)n24:15.4899)n16:9.21583)n13:27.7656,((n17:26.9607,((n37:7.25781,n38:7.25781)n34:10.14,n26:17.3978)n18:9.56292)n11:5.02306,(((n55:0.648497,n56:0.648497)n41:5.60308,n42:6.25157)n27:10.6186,((n35:7.35849,n36:7.35849)n31:5.41008,(n49:2.76193,n50:2.76193)n32:10.0066)n28:4.10161)n21:15.1136)n9:24.0297)n1:13.0768,(n43:5.22301,(n51:1.09491,n52:1.09491)n44:4.1281)n20:63.8673);", format=1)
codes = dict()

for node in mytree.traverse():
    if node.is_root():
        node.name = "Root"
        continue
    if not node.is_leaf():

        node.name = ""
        continue

    newname = "n" + str(int(node.name.replace("n","")) + 100000)
    codes[node.name] = newname
    node.name = newname



print(mytree.write(format=1))

myfiles = [x for x in os.listdir(mypath) if "pruned" in x]

for myfile in myfiles:
    print(myfile)
    with open(os.path.join(mypath, myfile)) as f:
        mytree = ete3.Tree(f.readline().strip(), format=1)
        root = mytree.get_tree_root()
        root.name = "Root"
        for node in mytree.iter_descendants():
            if node.is_leaf():
                continue
            node.name = ""
        for node in mytree.get_leaves():
            handle = node.name.split("_")
            newname = codes[handle[0]] + "_" + handle[1]
            node.name = newname

    with open(os.path.join(mypath, myfile.replace("_prunedtree.nwk", "_corrected")), "w") as f:
        f.write(mytree.write(format=1))


