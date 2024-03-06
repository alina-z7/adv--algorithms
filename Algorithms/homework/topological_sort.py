def in_degree(G, v):
  """Find the in-degree of vertex v in the input
  directed acyclic graph -- dag

  Inputs
  ------
  dag : list of lists
    adj list for input graph
  v : int
    a vertex in dag

  Returns
  int : the in-degree of v
  """

  # initialize count for in-degree - number of incoming edges for the vertex v
  in_degree = 0

  for vertex_list in G: # iterate through each vertex list in the graph G
    for neighbor in vertex_list: # iterate through each neighbor in the vertex list
      # if v seems to be in a vertex list (or it matches with a neighbor in the vertex list), 
      # it means there is an incoming edge from the list index i, 0 <= i <= len(G) - 1 for v
      if neighbor == v:
        # if so, increment in-degree count    
        in_degree += 1
        # return the in-degree for v
  return in_degree


def topo(G):
  """Find the in-degree of vertex v in the input
  directed acyclic graph -- dag

  Inputs
  ------
  dag : list of lists
    adj list for input graph; assume graph is acyclic and directed

  Returns
  int list:
    topological ordering of the graph's vertices
  """
  # initialize a dictionary to store key/value pairs of (vertex v, in_degree(G, v))
  topo_dict = {}
  # initialize vertex iterator for the graph G
  v = len(G) - 1

  # while we are in bounds of G with v
  while v >= 0:
    topo_dict[v] = in_degree(G, v) # store (v, in_degree(G, v)) for each v
    v -= 1 # go to next v
    # sort the dictionary pairs based on the in_degree values from min to max and store them in a new dictionary
  sort_dict = dict(sorted(topo_dict.items(), key=lambda x:x[1]))
  # return the list of topological sorted v's that are paired with the sorted in_degree values
  return list(sort_dict.keys())

# TEST
# This is the adjacency list of the graph used in the examples above.
G =[[1,2], # 0
    [3,4], # 1
    [4],   # 2
    [],    # 3
    [3]]   # 4
print(topo(G)) # Should return [0, 2, 1, 4, 3]