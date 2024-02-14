'''
optimal substructure - when you have the remaining parts with a sol
# P(i, j) = min[ P(i - 1, j - 1) + gamma_xiyi,
                P(i - 1, j) + gamma_gap,
                P(i, j - 1) + gamma_gap]

P(0,0) = 0 
P(i, 0) = i * gamma_gap
P(0, j) = j * gamma_gap

backtracking to find the sol with a min cost - dp
'''

def score(x, y):
    return 0 if x == y else 1

def penalty(X, Y, scoring_fun, gap_penalty):
    m = len(X)
    n = len(Y)
    P = [[0 for i in range(n+1) for i in range(m+1)]]
    # Initial conditions for X = empty
    for j in range(n+1):
        P[0][j] = j * gap_penalty
        # Initial consitions Y = empty
        for i in range(m+1):
            P[i][0] = i * gap_penalty
        # Build the rest of the P table
        for i in range(1, m+1):
            for j in range(1, n+1):
                x = X[i - 1] # # -1 to compensate for 0-based idx
                y = Y[j - 1] # ditto
            # What's the best deal here?
                P[i][j] = min(P[i - 1][j - 1] + scoring_fun(x, y), 
                          P[i - 1][j] + gap_penalty,
                          P[i][j - 1] + gap_penalty)
            return P
X = "BRAIN"
Y = "RAIN"
a_gap = 2
print(penalty(X, Y, score, a_gap))


print([[0 for j in range(n+1)] for i in range(m+1)])

print(score("A", "B"))