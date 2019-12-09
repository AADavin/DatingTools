import os
import sys
import ete3

def return_closest_marker(n):
    for i in range(2000):
        if n+i in n2marker and len(n2marker[n+i]) != 0:
            return(n+i)
        elif n-i in n2marker and len(n2marker[n-i]) != 0:
            return(n-i)
    return None

def select_markers(refpath, gtreepath):
    genetrees = [x for x in os.listdir(gtreepath) if "prun" in x]
    sgt2leaves = dict()
    for gt in genetrees:
        with open(os.path.join(gtreepath, gt)) as f:
            gtree = ete3.Tree(f.readline(),format=1)
    sgt2leaves[gt] = len(gtree)
    
    n2marker = dict()
    for k,v in sgt2leaves.items():
        if v not in n2marker:
            n2marker[v] = list()
        n2marker[v].append(k)
    
    genetrees = [x for x in os.listdir(refpath)]
    gt2leaves = dict()
    for gt in genetrees:
        with open(os.path.join(refpath, gt)) as f:
            gtree = ete3.Tree(f.readline(),format=1)
    sps = set([x.name for x in gtree])    
    gt2leaves[gt] = sps
    
    marker2match = dict()
    print("\t".join(["SELECTED_MARKER_SIZE", "REF_MARKER_SIZE","SELECTED_MARKER_NAME","REF_MARKER_NAME"]))
    for marker, leaves in gt2leaves.items():    
        y.append(len(leaves))
    
        if len(leaves) in n2marker and len(n2marker[len(leaves)]) >= 1:        
            x.append(len(leaves))
            match =  np.random.choice(list(n2marker[len(leaves)]))
            marker2match[marker] = match
            n2marker[len(leaves)] = [x for x in n2marker[len(leaves)] if x != match]
            print("\t".join([str(len(leaves)), str(len(leaves)), str(match), str(marker)]))
        else:
            cm = return_closest_marker(len(leaves))
            if cm == None:
                x.append(0)
            else:
                match =  np.random.choice(list(n2marker[cm]))
                print("\t".join([str(cm), str(len(leaves)), str(match), str(marker)]))
                marker2match[marker] = match
                n2marker[cm] = [x for x in n2marker[cm] if x != match]
                x.append(cm)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("usage: python select_markers.py refpath, genetreepath")
        exit(0)

    _, refpath, genetreepath  = sys.argv
    select_markers(refpath, genetreepath)

