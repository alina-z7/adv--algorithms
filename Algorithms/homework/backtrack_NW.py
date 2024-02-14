def score(x,y):
  """Naive match/mismatch scoring a_{xy} = 1 if x==y, 0 otherwise"""
  return 0 if x == y else 1

def needleman_wunch(X, Y, scoring, gap):
  """Computes the alignment penalties according to Needleman-Wunch.

  Inputs
  ------
  X : str
    First of two strings to be aligned
  Y: str
    Second of two strings to be aligned
  scoring : function
    The scoring function to be used. This is assumed to be a function that
    accepts two symbols are returns an int value of the missalignment
    penanlty. Function score, defined earlier, is a simple choice
  gap : int
    The penalty for a gap instead of a symbol in an alignment

  Returns
  -------
    P : list of lists
      The penalties for all alignment scenarios that minimize the cost
      of alignment using the gap and scoring values. In this table, the
      bottom-right cell P[m][n] is the minimum penantly of the best
      alignment possible. m, n are the lengths of the input strings X, Y.
  """
  # INITIALIZE
  # m,n shortcuts to length of strings, to simplify code
  m = len(X)
  n = len(Y)
  # Set up the array for computing total penalties. You may be tempted to
  # initialize array P = [[0] * n] * n. This will create shallow copies of
  # the inner arrays. The loop technique below creates deep copies, ie,
  # the inner arrays are independent of each other.
  P = [[0 for j in range(n+1)] for i in range(m+1)]
  # Set up the base case for j=0; this takes care of P[0][0] = 0
  for i in range(m+1):
    P[i][0] = i*gap
  # Set up the base case for i=0; this takes care of P[0][0] = 0, again!
  for j in range(n+1):
    P[0][j] = j*gap
  # COMPUTE P
  for i in range(1,m+1):
    for j in range(1,n+1):
      # Obtain i-th, j-th string characters; -1 compensate for 0-based indexing
      x = X[i-1]
      y = Y[j-1]
      # P is the best of three possible scenarios
      P[i][j] = min(
          P[i-1][j-1]+scoring(x,y), # scenario 1, letter over letter in last col
          P[i-1][j]+gap,            # scenario 2, gap over letter in last col
          P[i][j-1]+gap)            # scenario 3, letter over gap in last col
  return P


def backtrack_NW(X, Y, P, score, gap):
    m, n = len(X), len(Y) # get m and n for the lengths of the strs
    
    # initializing aligned strs
    x_aligned = "" 
    y_aligned = ""

    # while we don't hit the top left cell of P(0,0)
    while m > 0 or n > 0:
        current_cost = P[m][n] # start at the bottom right cell to evaluate costs P(m, n)
        cost_options = [
            P[m - 1][n] + gap, # cost of the left cell
            P[m][n - 1] + gap, # cost of the upper cell
            P[m - 1][n - 1] + score(X[m - 1], Y[n - 1]) # cost of the diagnol cell
        ]

        if current_cost == cost_options[0]:  # if the current cost matches the left cell
            x_aligned = X[m - 1] + x_aligned # concatenate the rightmost letter of X to X'
            y_aligned = "-" + y_aligned      # and a hyphen of Y to Y' to consider the gap cost
            m -= 1 # decrement m for next letter
        elif current_cost == cost_options[1]: # if the current cost matches the upper cell
            x_aligned = "-" + x_aligned       # concatenate a hyphen of X to X' to consider gap cost
            y_aligned = Y[n - 1] + y_aligned  # and the rightmost letter of Y to Y'
            n -= 1 # decrement n for next letter
        else:                                 # else the current cost matches the diagnol cell
            x_aligned = X[m - 1] + x_aligned  # concatenate the rightmost letter of Y to Y'
            y_aligned = Y[n - 1] + y_aligned  # and the rightmost letter of X to X'
            m -= 1 # decrement m for next letter
            n -= 1 # decrement n for next letter

    # Done - return aligned strs
    return x_aligned, y_aligned

# Test cases: X -> Y
def run_tests():
    test_dict = {
        'ASTRONOMY': 'GASTRONOMY',
        'CAT': 'DOG', 
        'CRANE': 'RAIN', 
        'CHICKEN': 'KITCHEN', 
        'CATS': 'SURF',
        'CYCLE':'BICYCLE',
        'GANDER':'AND',
        'TEAM':'TEA',
        'SEAL':'SEA'
    }
    gap = 0.5
    for X, Y in test_dict.items():
        P = needleman_wunch(X, Y, score, gap)
        print(backtrack_NW(X, Y, P, score, gap))

run_tests()


