def reachability(s, G):
    reachable = [] # list to return
    bag = [s] # our stack
    while bag:
        u = bag.pop() # pull something out of the bag
        if u not in reachable:
            reachable.append(u)
            for v in G[u]:
                bag.append(v)
    return reachable

G = [
    [1],
    [4, 5],
    [4],
    [2, 4, 5],
    [],
    [],
    [],
    [6]
]

print(reachability(3, G))