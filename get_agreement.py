from ete3 import PhyloTree
import sys

def get_constraints(constraints_file):

    constraints = dict()
    total_w = float()

    with open(constraints_file) as f:

        for line in f:

            dn,rc,wt = line.strip().split("\t")

            if dn not in constraints:
                constraints[dn] = dict()

            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0

            constraints[dn][rc] += float(wt)
            total_w += float(wt)

    return (constraints, total_w)

def compute_agreement(node_order, constraints):

    conflict = float()
    ranking = {node:rank for rank,node in enumerate(node_order)}
    for dn,rcs in constraints.iteritems():
        for rc,wt in rcs.iteritems():
            if ranking[dn] > ranking[rc]:
                conflict += wt

    return conflict


def get_agreement(*args):

    input_files = args[0]

    constraints_infile = input_files[0]
    sampling_frequency = int(input_files[1])
    node_orders_files = input_files[2:]

    constraints, total_weight = get_constraints(constraints_infile)

    agreements = list()

    for node_order_file in node_orders_files:

        name = node_order_file.split(".")[0]
        with open(node_order_file) as f:
            for i,order in enumerate(f):
                if i % sampling_frequency == 0:
                    myorder = order.strip().split(",")
                    try:
                        agreement = str(1-(compute_agreement(myorder, constraints)/total_weight))
                        agreements.append((agreement, name))
                    except:
                        agreements.append(["ERROR PROCESSING LINE"])


    print("Agreement,Type")
    for item in agreements:
        line = ",".join(item)
        print(line)



if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print ("usage: python get_agreement.py constraints_infile sampling_frequency orders1 orders2 ... ordersn")
        exit(0)

    get_agreement(sys.argv[1:])
