import sys
import numpy as np

def read_orders(orders_file):

    orders = list()

    with open(orders_file) as f:
        for line in f:
            order = line.strip().split(",")
            orders.append(order)

    return orders



def compute_variance(orders):

    node2range = dict()
    node2variance = dict()

    for order in orders:
        for i, node in enumerate(order):
            if node not in node2range:
                node2range[node] = list()
            node2range[node].append(i)

    for node, ranges in node2range.items():
        var = np.var(ranges)
        try:
            node2variance[node] = var
        except:
            node2variance[node] = 0

    return node2variance









def compute_convergence(random_file, chain_file, variance_ratio):

    rorders = read_orders(random_file)
    corders = read_orders(chain_file)

    r_node2variance = compute_variance(rorders)
    c_node2variance = compute_variance(corders)

    nodes = list(r_node2variance.keys())

    for n in nodes:

        try:
            ratio = r_node2variance[n] / c_node2variance[n]
            if ratio >= variance_ratio:
                r = "Yes"
            else:
                r = "No"

            print("\t".join(map(str, [n, r_node2variance[n], c_node2variance[n], ratio, r])))

        except:
            print("\t".join(map(str, [n, r_node2variance[n], c_node2variance[n], "NA", "NA"])))



if __name__ == "__main__":

    if len(sys.argv) != 1:
        print("usage: python compute_convergence.py random.orders yourchain.orders variance_ratio")
        exit(0)

    _, random_file, chain_file, variance_ratio = sys.argv
    compute_convergence(random_file, chain_file, float(variance_ratio))
