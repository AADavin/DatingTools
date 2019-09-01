# MaxTiC: Fast ranking of a phylogenetic tree by Maximum Time Consistency with lateral gene transfers
#
#
# python code written by Eric Tannier, Inria
# Using ideas, comments, suggestions from Cedric Chauve, Akbar Rafiey, Adrian A. Davin, Celine Scornavacca, Philippe Veber, Bastien Boussau, Gergely J Szollosi, Vincent Daubin
#
# Software distributed under the cecill licence, rights and permissions are described here:
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Bug reports, suggestions or help request for usage of MaxTic should be sent to eric.tannier@inria.fr
#
# If you use this software please cite
# MaxTiC: Fast ranking of a phylogenetic tree by Maximum Time Consistency with lateral gene transfers, Biorxiv doi.org/10.1101/127548 


import sys,script_tree,random,time,math

MAX_NUMBER = 10000000000
time0 = time.time()

parameters = sys.argv[1:]

if len(parameters) < 2:
  print "usage: python kendall.py species_tree_file1 species_tree_file2"
  exit()

for p in parameters[2:]:
  words = p.split("=")
  if words[0] == "t":
    TEMPERATURE = float(words[1])
  elif words[0] == "r":
    RANDOM_TYPE = int(words[1])
  elif words[0] == "ls":
    TIME_FOR_SEARCH = float(words[1])
  elif words[0] == "d":
    MIN_TRANSFER_DIST = int(words[1])
  elif words[0] == "rd":
    RANDOM = int(words[1])
  elif words[0] == "ts":
    THRESHOLD_CONSTRAINTS = float(words[1])
  else:
    print "unused parameter (bad format):",p


tree = script_tree.readTree(open(parameters[0],"r").readline())
root = script_tree.getRoot(tree)

tree1 = script_tree.readTree(open(parameters[0],"r").readline())
tree2 = script_tree.readTree(open(parameters[1],"r").readline())


root1 = script_tree.getRoot(tree1)
root2 = script_tree.getRoot(tree2)


def maximum_spearman(n):
  if n % 2 == 0:
    m = n /2
    return 2 * m * m
  else:
    m = (n-1)/2
    return 2 * m * m + 2 * m

def maximum_distance(tree,root):
  c1 = script_tree.getChildren(tree,root)[0]
  c2 = script_tree.getChildren(tree,root)[1]
  name = script_tree.getBootstrap(tree,root)
  if script_tree.isLeaf(tree,c1) and script_tree.isLeaf(tree,c2):
    return [[name],[name]]
  elif script_tree.isLeaf(tree,c1):
    oo = maximum_distance(tree,c2)
    return [[name] + oo[0],[name] + oo[1]]
  elif script_tree.isLeaf(tree,c2):
    oo = maximum_distance(tree,c1)
    return [[name] + oo[0],[name] + oo[1]]
  else:
    orders1 = maximum_distance(tree,c1)
    orders2 = maximum_distance(tree,c2)
    return [[name] + orders1[0] + orders2[0],[name] + orders2[1] + orders1[1]]

def spearman_distance(A,B):
  result = 0.0
  Binv = {}
  for i in range(len(B)):
    Binv[B[i]] = i
  #print len(Binv.keys()),len(A)
  for i in range(len(A)):
    j = Binv[A[i]]
    #print i,j,A[i]
    result = result + abs(i-j)
  #print maximum_spearman(len(A)),result
  return result

def spearman_similarity(A,B):
  m = maximum_distance(tree,script_tree.getRoot(tree))
  #print m,A,B
  #print spearman_distance(m[0],m[1]),spearman_distance(A,B)
  #print (spearman_distance(m[0],m[1]) - spearman_distance(A,B))/(spearman_distance(m[0],m[1]))
  return (spearman_distance(m[0],m[1]) - spearman_distance(A,B))/(spearman_distance(m[0],m[1]))

def kendall_distance(A,B):
  result = 0.0
  Ainv = {}
  for i in range(len(A)):
    Ainv[A[i]] = i
  Binv = {}
  for i in range(len(B)):
    Binv[B[i]] = i
  for i in range(len(A)):
    for j in range(i+1,len(A)):
      if Binv[A[i]] > Binv[A[j]]:
	result = result + 1
  return result

def kendall_similarity(A,B):
  m = maximum_distance(tree,script_tree.getRoot(tree))
  #print m
  #print kendall_distance(m[0],m[1]) , kendall_distance(A,B)
  return (kendall_distance(m[0],m[1]) - kendall_distance(A,B))/(kendall_distance(m[0],m[1]))

def similarity(A,B):
  #return spearman_similarity(A,B)
  return kendall_similarity(A,B)

def path(g,a,b):  # is there a directed path in graph g from a to b, true if a=b
        marques = [a]
        pile = [a]
        while len(pile) > 0 and (not (b in marques)):
                sommet = pile[-1]
                del pile[-1]
                voisins = g[sommet]
                for v in voisins:
                        if not v in marques:
                                marques.append(v)
                                pile.append(v)
        if b in marques:
                return True
        else:
                return False


def tree_from_order(order):
  nodes = script_tree.getNodes(tree)
  for n in nodes:
    if not script_tree.isRoot(tree,n):
      if script_tree.isLeaf(tree,n):
	index = len(order)
      else:
	index = order.index(script_tree.getBootstrap(tree,n))
      index_parent = order.index(script_tree.getBootstrap(tree,script_tree.getParent(tree,n)))
      script_tree.setLength(tree,n,index-index_parent)

  return script_tree.writeTree(tree,root,False)

def order_from_graph(graph):
  result = []
  marques = {}
  for l in script_tree.getLeavesNames(tree):
    marques[l] = 0
  while len(result) < len(graph.keys()) - len(script_tree.getLeavesNames(tree)):
    keys = graph.keys()
    i = 0
    while marques.has_key(keys[i]):
      i = i + 1
    current = keys[i]
    suivant = True
    while suivant:
      suivant = False
      for v in graph[current]:
	if not marques.has_key(v):
	  suivant = True
	  current = v
    result.append(current)
    marques[current] = 0
  result.reverse()
  return result
  
  while len(graph[current]) > 0:
    current = graph[current][0]
    result.append(current)
  return result

def optimisation_locale(order,duration):
  #sortie_tree = open("MT_output_tree_sample","w")
  #sortie_val = open("MT_output_score_sample","w")
  time0=time.time()
  current = value(order)
  best = current
  best_order = list(order)
  sample = []
  #print ref
  while time.time() - time0 < duration:
    i = int(random.random()*(len(order)))
    j = int(random.random()*(len(order)))
    if i != j:
      essai = list(order)
      a = min(i,j)
      b = max(i,j)
      temp = essai[a]
      essai[a:b] = essai[a+1:b+1]
      essai[b] = temp
      v = value(essai)
      if v < MAX_NUMBER:
	#sortie_tree.write(tree_from_order(order)+" "+str(current)+" "+str(TEMPERATURE)+"\n")
	#sortie_val.write(str(current)+"\n")
	if v <= current:
	  metropolis_ratio = 1
	  #TEMPERATURE = min(0.01,TEMPERATURE/10)
	else:
	  metropolis_ratio = math.exp((current-v)/TEMPERATURE)
	coin = random.random()
	if coin < metropolis_ratio:
	  order = essai
	  current = v
	if v < best:
          print "better solution",v  
	  best = v
	  best_order = list(order)
	  sample = []
	if v == best and len(sample) < 10000:
	  sample.append(similarity(order_input,order))
	  
  #sortie_val = open("MT_output_score_sample","w")
  #for s in sample:
    #sortie_val.write(str(s)+"\n")
  return best_order
    

def edgeweights(element,elements):
  result = 0
  for s in degre_entrant[element]:
    if s in elements:
      if edge.has_key(s+","+element):
	result = result + edge[s+","+element]
  return result

def mix(order1,order2):
  order = []
  cost = [[0]*(len(order2)+1)] 
  for i in range(1,len(order1)+1):
    cost.append([0]*(len(order2)+1))
  back = [["j"]*(len(order2)+1)] 
  for i in range(1,len(order1)+1):
    back.append(["i"]+[""]*(len(order2)))
  for i in range(1,len(order1)+1):
    for j in range(1,len(order2)+1):
      #print i,j,len(order1),len(order2)
      value1 = cost[i-1][j] + edgeweights(order1[i-1],order2[0:j])
      value2 = cost[i][j-1] + edgeweights(order2[j-1],order1[0:i])
      if value1 == value2:
        x = random.random()
        if x < 0.5:
          cost[i][j] = value1
          back[i][j] = "i"
        else:
          cost[i][j] = value2
          back[i][j] = "j"
      elif value1 < value2:
        cost[i][j] = value1
        back[i][j] = "i"
      else:
        cost[i][j] = value2
        back[i][j] = "j"
  i = len(order1)
  j = len(order2)
  while i>0 or j>0:
    if back[i][j] == "i":
      #print i,len(order1)
      order.append(order1[i-1])
      i = i - 1
    else:
      order.append(order2[j-1])
      j = j - 1
  order.reverse()
  return order
     
def opt(tree,root):
  if (script_tree.isLeaf(tree,script_tree.getChildren(tree,root)[0]) and
      script_tree.isLeaf(tree,script_tree.getChildren(tree,root)[1])):
    return [script_tree.getBootstrap(tree,root)]
  elif script_tree.isLeaf(tree,script_tree.getChildren(tree,root)[0]):
    return opt(tree,script_tree.getChildren(tree,root)[1])+[script_tree.getBootstrap(tree,root)]
  elif script_tree.isLeaf(tree,script_tree.getChildren(tree,root)[1]):
    return opt(tree,script_tree.getChildren(tree,root)[0])+[script_tree.getBootstrap(tree,root)]
  else:
    order1 = opt(tree,script_tree.getChildren(tree,root)[0])
    order2 = opt(tree,script_tree.getChildren(tree,root)[1])
    #print "level",len(order1)+len(order2),order1,order2
    return mix(order1,order2) + [script_tree.getBootstrap(tree,root)]
  

def random_order(tree,root):
  c1 = script_tree.getChildren(tree,root)[0]
  c2 = script_tree.getChildren(tree,root)[1]
  name = script_tree.getBootstrap(tree,root)
  if script_tree.isLeaf(tree,c1) and script_tree.isLeaf(tree,c2):
    return [name]
  elif script_tree.isLeaf(tree,c1):
    return [name] + random_order(tree,c2)
  elif script_tree.isLeaf(tree,c2):
    return [name] + random_order(tree,c1)
  else:
    order1 = random_order(tree,c1)
    order2 = random_order(tree,c2)
    #if script_tree.isRoot(tree,root):
      #print order1,order2
    pos = range(len(order1)+len(order2))
    for i in range(len(order2)):
      index = int(random.random()*(len(pos)))
      del pos[index]
    #if script_tree.isRoot(tree,root):
      #print pos
    order = [name]
    previous = 0
    for i in pos:
      for j in range(i - previous):
	#if script_tree.isRoot(tree,root):
	  #print order2,i,previous
	order.append(order2[0])
	del order2[0]
      order.append(order1[0])
      del order1[0]
      previous = i+1
	
    #if script_tree.isRoot(tree,root):
      #print order1,order2,order
    return order + order2


def order_from_tree(tree):
  order = []
  nodes = script_tree.getNodes(tree)
  root = script_tree.getRoot(tree)
  for n in nodes:
    if not script_tree.isLeaf(tree,n):
      order.append(n)
  #print order
  order.sort(lambda x,y: cmp(script_tree.distanceFrom(tree,x,root),script_tree.distanceFrom(tree,y,root)))
  for i in range(len(order)):
    order[i] = script_tree.getBootstrap(tree,order[i])
  return order

# useful variables

nodes1 = script_tree.getNodes(tree1)
leaves1 = script_tree.getLeavesNames(tree1)
root1 = script_tree.getRoot(tree1)
internal_nodes1 = []

nodes2 = script_tree.getNodes(tree2)
leaves2 = script_tree.getLeavesNames(tree2)
root2 = script_tree.getRoot(tree2)
internal_nodes2 = []


order_input1 = order_from_tree(tree1)
order_input2 = order_from_tree(tree2)

#value_input = value(order_input)


print(similarity(order_input1 ,order_input2))





