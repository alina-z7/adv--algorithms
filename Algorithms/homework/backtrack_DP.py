# Simple test case, matches slide deck example at:
# https://docs.google.com/presentation/d/1fhhKnA9CH3AY_ltPt4qgtjsXocscWCf5C2cgxi4RCKw/edit?usp=sharing

import numpy as np # for nice array printing with np.matrix()

def dyn_prog(v, w, C):
  """Find the optimal value among n items under a constraint C using
  dynamic programming.

  Successive optimal solutions for problems of size 0 ≤ i ≤ n
  and for constraints 0 ≤ j ≤ C are computed, leading to the
  final optimal solution S[n][C].

  Inputs
  ------
  v : list
    Values of items we use to build optimal solution. For n items, this list
    is expected to have n+1 items. list[0] is not used, so that item value is
    synchronized with position index. First item is at [1] (instead of 0),
    second item at [2] (instead of 1), etc.
  w : list
    Weights of items we use to build optimal solution. For n items, this list
    is expected to have n+1 items. list[0] is not used, so that item weight is
    synchronized with position index. First item is at [1] (instead of 0),
    second item at [2] (instead of 1), etc.
  C : int
    Contraint for optimal solution; total weight of items in optimal
    solution cannot exceed C.

  Returns
  -------
  S : list
    All optimal solutions for subproblems  of size 0 ≤ i ≤ n and for
    constraints 0 ≤ j ≤ L. Ultimately we are only interested in the final
    optimal value S[n][L], but we need array S to backtrack and identify
    the items comprising the optimal solution
  """
  # List v (and w) has one extra element, since we are not using position [0]
  # to store any meaningful data. We skip position zero so that the data for
  # the first item will be at position [1], for the second at position [2], etc.
  # The actual number of items to process is the length-1.
  n = len(v) - 1
  # Initialize the S array. We need one extra row for the combinations among
  # zero items and an extra column for optimal solutions at zero capacity. These
  # values are trivial (S[i][0] = S[0][j] = 0) but imporant because they provide
  # the initial conditions for the algorithm.
  S = [ [0 for _ in range(C+1)] for _ in range(n+1)]
  # explore every combination of items and capacities
  for item in range(1, n+1): # Loop runs up to and including n
    for capacity in range(1, C+1): # Loop runs up to and including C
      # The weight of item.
      weight = w[item]
      # The value of item.
      value = v[item]
      # Optimal solution of previously smaller problem (with one item less)
      # at the same capacity.
      one_less_item = item - 1
      previous = S[one_less_item][capacity]
      if weight > capacity:
        # Current item weights more than present capacity. It cannot be added
        #  to solution, even if we removed everything to make room for it.
        # Simply there is no room. The optimal value at this capacity is
        # the optimal value for the smaller problem, with one less item
        # at same capacity.
        S[item][capacity] = previous
      else:
        # We are here because capacity ≥ current item weight. This means that
        # we can remove some items from the previous optimal solution to make
        # room for the current item. If we did so, the value of the optimal
        # solution can be found at the reduced capacity for the previously
        # smaller problem added to the value of the current item. The reduced
        # capacity is what remains after we make room for the current item.
        reduced = capacity - weight
        previous_at_reduced = S[one_less_item][reduced]
        S[item][capacity] = max(previous, value + previous_at_reduced)
        #                                 ------------------------
        #                                 Value of current item plus the value
        #                                 of previously smaller problem (with
        #                                 one less item) at the reduced capacity
        #                                 that is necessary in order to fit the
        #                                 current item.
  # Done, return the full array S.
  # The value for the optimal solution
  # is at S[n][C]. The full array is
  # needed in order to find the items
  # that comprise the optimal solution
  return S

def reconstruct(S,v,w):
  n, C = len(v) - 1, len(S[0]) - 1 # get n and C as the lengths of the item | capacity table
  best_loot_list = [] # initialize a list to store the best loot items in the optimal solution S(n, C)

  while n > 0 and C > 0: # while we don't hit the top left stump cells S(0,0)
    max_loot = S[n][C] # get the optimal value stored in S(n, C) with the maximum loot

    if max_loot != S[n - 1][C]: # if the value without the current item is different from the current maximum loot,
                                # then that item is a part of the optimal solution
      
      best_loot_list.append(n) # add the index of that item to the list, as it is loot option
      
      C -= w[n] # subtract the current weight of the item from the current capacity C
   
    n -= 1 # go to the next item

  return best_loot_list[::-1] # return the loot list in reverse order



C = 6
n = 4

w = [-1, 4, 3, 2, 1] # weights
v = [-1, 5, 4, 3, 2] # values
#     |  |  |  |  |
#    [0][1][2][3][4]
#     |  |  |  |  |
#     |  |  |  |  +--> 4th item weight w[4] and value v[4]
#     |  |  |  +-----> 3rd item weight w[3] and value v[3]
#     |  |  +--------> 2nd item weight w[2] and value v[2]
#     |  +-----------> 1st item weight w[1] and value v[1]
#     +--------------> not used -- stump value to allow us to use array
#                      elements 1 through n-inclusive, for data.

S=dyn_prog(v,w,C)
#print(np.matrix(S))
print(reconstruct(S,v,w))