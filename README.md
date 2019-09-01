
# Dating Tools
#### A collection of phylogenetic scripts to date using transfers


Clone this repo to your computer and use as you please


***

For using these scripts you will need to install the library ete3

`pip install ete3` 

You might need also six (a dependency of ete3)

`pip install six` 

***

* **bootstrap_constraints.py**

Bootstrap a file of transfers (read with parse transfers) and outputs a given number of replicates
from those transfers, sampling with replacement

* **count_orders.py**

It tells you how many ranked trees there are for a given tree. Thanks to Sebastián Izquierdo (https://es.wikipedia.org/wiki/Sebasti%C3%A1n_Izquierdo) for his help

* **compute_reds.py**

Computes the RED tree

* **get_constraints.py**

Prints the constraints given a set of transfers and a species tree

* **get_node_order.py**

Reads a tree, outputs the node order of the tree. The format is, from the oldest to the youngest separated by commas

* **get_agreement.py**

Receives a constraints file and a node orders file and returns the agreement

* **generate_orders.py**

Generates all the possible ranked trees for a given tree.
Watch out, for some trees the number of possibilities might be larger than the number of atoms in the universe.

* **map_trees.py**

Map the inner nodes of a reference tree to a set of trees

* **mc_explorer.py**

Explores ranked trees using a Bayesian approach.
You can use it to generate a set of trees compatible with a set of constraints by setting a very low temperature

* **parse_transfers.py**

Reads all the uTs files in your current file and prints all transfers

* **propagate_constraints.py**

Takes a species tree, a calibration file (PhyloBayes format) and a constraint file (.tsv, see TestFiles for an example)

Returns the annotated species tree in which the inner nodes are called:

UPPERCONSTRAINT_LOWERCONSTRAINT

* **read_bootstrap.py**

Reads a set of files (output of MaxTiC, partial order) and it gives you the number of times that a constraint was found

* **ultrametrice.py**

Receives a tree and a node order (see script get_node_order.py) and outputs the ultrametric tree with that node order
