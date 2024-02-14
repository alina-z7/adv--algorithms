'''

recursive method to multiply two strs, and return in str format
n = power of 2
x, y = n - digits

assert: x and y have to be the in the powers of 2

Formula:
x = a * 10 ^ n/2 + b
y = c * 10 ^ n/2 + d

x * y = ac * 10 ^ n + (bc + ad) * 10 ^ m + bd

hw: change the add_strs function to multiply the two strs without zero padding

'''


def multiply_strs(x, y):
    # x, y have numeric symbols only -- no need to check;
    # and their length is a power of 2;
    # no need to check either

    # Base case - x and y are length of 1
    if len(x) == len(y) == 1:
        return str(int(x) * int(y))
    # Recursive case x and y > 1
    else:
        # Split the strs into left and right halves
        n = len(x)  # current length of x and y
        m = n // 2  # half-length
        a = x[:m]  # left half of x
        b = x[m:]  # right half of x
        c = y[:m]  # left half of y
        d = y[m:]  # right half of y
        ac = multiply_strs(a, c)
        bc = multiply_strs(b, c)
        ad = multiply_strs(a, d)
        bd = multiply_strs(b, d)

        # product to return, as str:
        # x * y = ac * 10 ^ n + (bc + ad) * 10 ^ m + bd
        bcad = add_str(bc, ad)
        ac10n = ac + "0" * n  # padding ac * 10 ^ n with zeros
        bcad10m = bcad + "0" * m  # (bc + ad) * 10 ^ m padding with zeros
        res = add_str(add_str(ac10n, bcad10m), bd)  # adding ac * 10 ^ n and (bc + ad) * 10 ^ m and bd
    return res


'''
adding strs function

add(x, y):
carry = 0
    for i = len(x) - 1...0
    num_x = int(x[i])
    num_y = int(y[i])
'''


def add_str(x, y):
    if len(x) != len(y):
        max_len = max(len(x), len(y))
        x = "0" * (max_len - len(x)) + x
        y = "0" * (max_len - len(y)) + y
    added_str = ""
    carry = 0
    n = len(x)
    for i in range(n - 1, -1, -1):
        x_num = int(x[i])
        y_num = int(y[i])
        sum = carry + x_num + y_num
        carry = sum // 10
        sum = sum % 10
        added_str = str(sum) + added_str

        if carry > 1:
            added_str = "1" + added_str
    return added_str

x = "1234"
y = "5678"

print(multiply_strs(x, y))  # should print 7006652
