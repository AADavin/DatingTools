# Now we go over constraints and we count the number of trees that respect this constraint
import sys

def get_constraints(constraints_file):

    constraints = dict()
    total_w = float()

    with open(constraints_file) as f:

        for line in f:

            dn,rc,wt,ig = line.strip().split(" ")

            if dn not in constraints:
                constraints[dn] = dict()

            if rc not in constraints[dn]:
                constraints[dn][rc] = 0.0

            constraints[dn][rc] += float(wt)
            total_w += float(wt)

    return (constraints, total_w)

def compute_agreement(dn,rc,orders):

    agreement = float()
    total = float(len(orders))

    for node_order in orders:
        ranking = {node:rank for rank,node in enumerate(node_order.split(","))}
        if ranking[dn] < ranking[rc]:
            agreement += 1

    return agreement/total


def get_agreement(*args):

    input_files = args[0]

    constraints_infile = input_files[0]
    sampling_frequency = int(input_files[1])
    node_orders_files = input_files[2:]

    constraints, total_weight = get_constraints(constraints_infile)

    orders = dict()

    for node_order_file in node_orders_files:
        name = node_order_file.split("_")[1]
        with open(node_order_file) as f:
            orders[name] = list()
            for i,line in enumerate(f):
                if i % sampling_frequency == 0:

                    orders[name].append(line.strip())

    data = list()

    header = list()
    header.append("DN")
    header.append("RC")
    header.append("WT")
    for item in orders.keys():
        header.append(item)

    header = "\t".join(header)
    print (header)


    for dn, rcs in constraints.iteritems():
        for rc, wt in rcs.iteritems():

            #line =",".join(map(str,[dn, rc, compute_agreement(dn,rc,v), k]))
            line = list()
            line.append(dn)
            line.append(rc)
            line.append(wt)

            for t in orders.keys():
                line.append(compute_agreement(dn,rc,orders[t]))

            line = "\t".join(map(str,line))
            print(line)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print ("usage: python get_agreement.py constraints_infile sampling_frequency orders1 orders2 ... ordersn")
        exit(0)

    get_agreement(sys.argv[1:])