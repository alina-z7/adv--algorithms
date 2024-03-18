'''
From my understanding, the Ford-Fulkerson algorithm does the following simple terms:

    1. While there are enough paths from the src to sink
    2. Add the minimum capactiy of each path to the overall maximum capacity
    3. Saturate the other edges of that path by subtracting the current capacity with the minimum capacity
    4. Returns the maximum capacity

    1, 2, 3 can be broken into specialized methods:

        1 - Depth First Search (DFS)
        2 - Ford Fulkerson Max Flow Finder
        3 - Residual Graph Saturation 
    
    (Ford Fulkerson method can be made to return the max flow)
    
'''
def ford_fulkerson_max_flow(G, src, sink):
# main method to calculate max flow using the Ford-Fulkerson algorithm
    
    max_flow = 0 # initialize max flow to zero
    R = initial_residual_graph(G) # initialize the residual graph R

    while True: # while there will be aug paths in the graph, which will be determined by DFS

        bitmap = [False] * len(G) # bitmap - to mark visited vertices v in G,
                                  # now initialized to False list

        flow_path_list = [] # available flow paths list for path tracking
        flow_path_list.append(src) # start from the src 

        # find the aug path through DFS and the current flow available
        aug_path, flow = dfs(R, src, sink, bitmap, flow_path_list)

        # if there is an aug path
        if aug_path:

            max_flow += flow # add the curr flow to max flow

            # since this is true, we take the flow and the path to saturate the the other edges in the path
            # by updating the residual graph accordingly
            saturate_residual_graph(R, flow_path_list, flow)

        else:

            break # else there is no aug path, forget it

    return max_flow # return the max flow

def initial_residual_graph(G): # initialize R to G (matching capacities and vertices)
    R = G
    return R

def dfs(G, src, sink, bitmap, flow_path_list): # DFS - finding aug path from src -> sink

    if src == sink: # Base case: if we end up at the sink, then we need to finish up with the search

        min_flow = float('inf') # initialize min flow to inf
        for path in range(len(flow_path_list) - 1): # for every path in the path list

            u = flow_path_list[path] # get the u vertex
            v = flow_path_list[path + 1] # get the v vertex

            # compare the current min flow in the path with the current flow of G(u, v)
            # set the min flow with the min capacity
            min_flow = min(min_flow, G[u][v]) 

        return (True, min_flow) # return True that there is a path and the min flow for the aug path
    
    # Recursive case: we keep looking for the augmenting path by visiting the other vertices
    bitmap[src] = True # Let's start by marking the src as visited

    for v in range(len(G)): # then for every vertex in G

        if not bitmap[v] and G[src][v] > 0: 
            # if that vertex is not visited and its capacity is non-zero,
                # there is a path
                        # add that vertex to the flow path list
            flow_path_list.append(v)

            # keep going - until we reach the sink from the current vertex we are on which is the new src
            aug_path, flow = dfs(G, v, sink, bitmap, flow_path_list)

            # if there is now an aug path 
            if aug_path:
                # let's return that
                return (True, flow)
            # remove the latest vertex in every search
            flow_path_list.pop()
    
    return (False, 0) # if we reached here, then there is no aug path and no current flow

def saturate_residual_graph(R, flow_path_list, flow): # saturation method
    # after we make sure that there is an aug path, 
    # we need to update R and saturate the path with the min flow capacity edge

    for path in range(len(flow_path_list) - 1): # for every path in the path list

        u = flow_path_list[path] # get the u vertex
        v = flow_path_list[path + 1] # get the v vertex

        R[u][v] -= flow # update R(u,v) and R(v, u) based on the edge capacities
        R[v][u] += flow # v -> u || u -> v


# Test graph
G = [
    [0, 20, 0, 0, 0], # A
    [0, 0, 5, 6, 0],  # B
    [0, 0, 0, 3, 7],  # C
    [0, 0, 0, 0, 8],  # D
    [0, 0, 0, 0, 0]   # E
]

src = 0 # starting vertex A
sink = len(G) - 1 # ending vertex E

print(ford_fulkerson_max_flow(G, src, sink))  # should return 11