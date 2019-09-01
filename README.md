
# Dating Tools
#### A collection of phylogenetic scripts to date using transfers


Clone this repo to your computer and use as you please


***

For using these scripts you will need to install the library ete3

`pip install ete3` 

You might need also six (a dependency of ete3)

`pip install six` 

***

* **parse_transfers.py**

Reads all the uTs files in your current file and prints all transfers

* **get_node_order.py**

Reads a tree, outputs the node order of the tree. The format is, from the oldest to the youngest separated by commas

* **propagate_constraints.py**

Takes a species tree, a calibration file (PhyloBayes format) and a constraint file (.tsv, see TestFiles for an example)

Returns the annotated species tree in which the inner nodes are called:

UPPERCONSTRAINT_LOWERCONSTRAINT

* **mc_explorer.py**

Explores ranked trees using a Bayesian approach.
You can use it to generate a set of trees compatible with a set of constraints by setting a very low temperature

* **count_orders.py**

It tells you how many ranked trees there are for a given tree. Thanks to Sebastián Izquierdo for his help 

* **generate_orders.py**

Generates all the possible ranked trees for a given tree.
Watch out, for some trees the number of possibilities might be larger than the number of atoms in the universe.
