#Given an undirected, weighted graph G:
#Initialize T as a copy of G with all its vertices and none of its edges.

#while T has more than one component:
#  Count components and label all vertices in T with their component.
#  Assume there are no safe edges out of any component in T.
#  for every edge (u,v) in G and u,v are in different components of T:
#    if there is no safe edge out of component with vertex u:
#      make (u,v) the safe edge out of component with vertex u.
#    else:
#      if weight(u,v) < weight of current safe edge out of component with vertex u:
#        make (u,v) the safe edge out of component with vertex u.
#    if there is no safe edge out of component with vertex v:
#      make (v,u) the safe edge out of component with vertex v
#    else:
#      if weight(v,u) < weight of current safe edge out of component with vertex v:
#        make (v,u) the safe edge out of component with vertex v.
#  add safe edges to T
# T is the Minimum Spanning Tree of G.

import threading
import time

# Function to print numbers from 1 to 5
def print_numbers():
    for i in range(1, 6):
        print("Thread 1:", i)
        time.sleep(1)  # Simulate some time-consuming task

# Function to print letters from 'a' to 'e'
def print_letters():
    for char in 'abcde':
        print("Thread 2:", char)
        time.sleep(1)  # Simulate some time-consuming task

# Create two threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both threads have finished execution")


from mst.mst import count_and_label
from mst.mst import initialize_tree_of


#Test

_  = 9999

G = [  #0   1   2   3   4   5   <---- column labels
      [ _,  _,  _,  5,  1,  _], # 0 \
      [ _,  _, 20,  5,  _, 10], # 1  \
      [ _, 20,  _, 10,  _,  _], # 2   row
      [ 5,  5, 10,  _,  _, 15], # 3   labels
      [ 1,  _,  _,  _,  _, 20], # 4  /
      [ _,  10, _, 15, 20,  _]  # 5 /
]

def minimum_spanning_tree(G):
    T = initialize_tree_of(G)
    count, comp = count_and_label(G)
    while count > 1:
        safe = [None] * [count + 1]
    
    for u in range(len(G)):
        for v in range(len(G)):
            if G[u][v] < G[0][0]:
                if comp[u] != comp[v]: # components are diff vals
                    if safe[comp[u]] is None:
                        safe[comp[u]] = [u, v]
                    else:
                       curr_safe_edge = safe[comp[u]] 
                       x, y = curr_safe_edge[0], curr_safe_edge[1]
                       curr_weight = G[x][y]
                       if G[u][v] < curr_weight:
                           safe[comp[u]] = [u, v]

                    if safe[comp[v]] is None:
                        safe[comp[v]] = [v, u]
                    else:
                       curr_safe_edge = safe[comp[v]] 
                       x, y = curr_safe_edge[0], curr_safe_edge[1]
                       curr_weight = G[x][y]
                       if G[v][u] < curr_weight:
                           safe[comp[v]] = [v, u]


        # add the safe edges to T
        for i in range(1, count + 1):
            safe_edge = safe[i]
            x = safe_edge[0]     
            y = safe_edge[1]
            T[x][y] = G[x][y]
            T[y][x] = G[y][x]
        count, comp = count_and_label(T)
    return T # T is the MST of G