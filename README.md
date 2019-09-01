
# Dating Tools
#### A collection of phylogenetic scripts to date using transfers


Clone this repo to your computer and use as you please


***

For using these scripts you will need to install the library ete3

`pip install ete3` 

You might need also six (a dependency of ete3)

`pip install six` 

***

* propagate_constraints.py

Takes a species tree, a calibration file (PhyloBayes format) and a constraint file (.tsv, see TestFiles for an example)

Returns the annotated species tree in which the inner nodes are called:

UPPERCONSTRAINT_LOWERCONSTRAINT

