import time
import random
import math
import pandas as pd 
import matplotlib.pyplot as grph
import sys

sys.set_int_max_str_digits(0)

def mult_str(x,y):
    """ Performs basic multiplication between two non-negative integers that
    are represented as strings whose length must be a power of 2.

    Inputs
    ------
    x, y : string
      Strings containing the integers to multiply. Must be non-negative and with
      2, 4, 8, 16,...2^p digits.

    Returns
    -------
    string
      With the integer that corresponds to the product x*y
    """
    if len(x) == len(y) == 1:
        # Base case! We can pull the integer digit out of the string,
        # perform single-digit multiplication, and return the product
        # represented as a string.
        return str(int(x)*int(y))
    else:
        # Split strings into left and right halves
        n = len(x) # current length of x and y
        m = n//2   # half length      #  Here we use fancy Python slicing
        a = x[:m]  # left half of     #  ommitting the beginning of the
        b = x[m:]  # right half of x  #  string if the slice starts there,
        c = y[:m]  # left half of y   #  i.e., x[0:m] same as x[:m]. Ditto for
        d = y[m:]  # right half of y  #  x[m:n] = x[m:], when n = last char.

        # Compute the four products needed, recursively
        ac = mult_str(a,c)
        bc = mult_str(b,c)
        ad = mult_str(a,d)
        bd = mult_str(b,d)

        # Compute the parts of ac*10^n+(bc+ad)*10^m+bd. Here, additions can be
        # performed as str-int-str conversions for simplicity. Multiplications
        # by a power of 10 is done by adding the necessary number of zeros to
        # the right of the string.

        bcad = str(int(bc)+int(ad)) # bc+ad
        ac10n = ac + "0"*n # multiply ac by 10^n by adding n zeros after it
        bcad10m = bcad + "0"*m #  multiply ac by 10^m by adding m zeros after it

        # Done
        return str(int(ac10n)+int(bcad10m)+int(bd))

def karatsuba_strs(x, y): 

    if len(x) == len(y) == 1:
       # Base case - x and y are length of 1, add them and convert back to str
        return str(int(x) * int(y))
    else:
        # take the max length for equal alignment
        max_len = max(len(x), len(y))

        #base_2_power = 2 ** (math.ceil(math.log2(max_len)))
        
        # get the power of two greater or equal to the length of the max
        #base_2_power = 2 ** (max_len - 1).bit_length()
        #print(base_2_power)
        if max_len % 2 == 1:
            max_len += 1

        # pad x and y with zeros to make 2^n length
        x = "0" * (max_len - len(x)) + x
        y = "0" * (max_len - len(y)) + y

        # Recursive case x and/or y length > 1
        # Split the strs into left and right halves
        n = len(x) # current length of x and y
        m = n // 2 # half-length

        a = x[:m] # left half of x
        b = x[m:] # right half of x
        c = y[:m] # left half of y
        d = y[m:] # right half of y

        ac = karatsuba_strs(a, c) # recursively multiply a and c
        bd = karatsuba_strs(b, d) # recursively multiply b and d

        # (𝑎+𝑏)(𝑐+𝑑)−𝑎𝑐−𝑏𝑑 calculation 
        a_plus_b_x_c_plus_d = karatsuba_strs(str(int(a) + int(b)), str(int(c) + int(d)))
        a_plus_b_x_c_plus_d_rm = str(int(a_plus_b_x_c_plus_d) - int(ac) - int(bd))

        ac10n = ac + "0" * n # padding ac * 10 ^ n with zeros
        a_plus_b_x_c_plus_d_rm10m = a_plus_b_x_c_plus_d_rm + "0" * m # padding (𝑎+𝑏)(𝑐+𝑑)−𝑎𝑐−𝑏𝑑 with zeros

        # Done
        return str(int(ac10n) + int(a_plus_b_x_c_plus_d_rm10m) + int(bd))

def print_comparison_table():
    data = {'n': [], 'T(n) plain' : [], 'T(n) Karatsuba' : []}

    for n in range(1, 14):
        x_digits = []
        y_digits = []

        for _ in range(2 ** n):
            x_digits.append(str(random.randint(0, 9)))
        x = "".join(x_digits)

        for _ in range(2 ** n):
            y_digits.append(str(random.randint(0, 9)))
        y = "".join(y_digits)

        startTimeM = time.time()
        mult_str(x, y)
        stopTimeM = time.time()

        startTimeK = time.time()
        karatsuba_strs(x, y)
        stopTimeK = time.time()

        data['n'].append(2 ** n)
        data['T(n) plain'].append(stopTimeM - startTimeM)
        data['T(n) Karatsuba'].append(stopTimeK - startTimeK)
        
        dataFrame = pd.DataFrame(data)

    print(dataFrame)

    

    grph.figure("Plain vs. Karatsuba Multiplication Analysis Chart")
    grph.title('Plain vs. Karatsuba Multiplication')

    grph.xlabel('n')
    grph.ylabel('Time (s)')

    grph.xscale('log', base=2)
    grph.yscale('log')

    grph.plot(dataFrame['n'], dataFrame['T(n) plain'], marker='o', label='Plain Integer Multiplication')
    grph.plot(dataFrame['n'], dataFrame['T(n) Karatsuba'], marker='o', label='Karatsuba Multiplication')
    
    grph.legend()
    grph.show()


print_comparison_table()

print(mult_str("12345678", "87654321"))
print(karatsuba_strs("12345678", "87654321"))
