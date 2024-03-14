'''
Input:
msg -> ASCII en

Output:
Compressed text message + encoding table

Initialize: forest with root-only tree (i.e., single nodes) symbols & freq

While forest has more than one node:
    remove the two nodes w/ lowest freq
    combine them as children of a new node whose value is their total freq
'''
msg = "HELLO WORLD"

def get_freq_dict(msg):
    freq = {}
    for l in msg:
        if l in freq:
            freq[l] += 1
        else:
            freq[l] = 1
    return freq

def get_freq(msg):
    space = ord(' ')
    tilde = ord('~')
    from_space_to_tilde = tilde - space

    freq = [0] * from_space_to_tilde

    if msg not in None and len(msg) > 0:
        for sym in msg:
            sym_ascii = ord(sym)
            if space <= sym_ascii <= tilde:
                freq[sym_ascii] += 1
    return freq

class Huffman_Node:

    def __init__(self, freq, sym=None):
        self.sym = sym
        self.freq = freq
        self.left = None
        self.right = None
    
    def _lt_(self, other):
        return self.freq < other.freq
    

f = get_freq_dict(msg)
forest = []
for sym in f:
    freq = f[sym]
    node = Huffman_Node(f[sym], sym)
    forest.append(node)

def lowest_freq_node(forest):
    lfn = forest[0]
    for i in range(1, len(forest)):
        if forest[i] < lfn:
            lfn = forest[i]
            pos_lfn = i

    return forest.pop(pos_lfn)

t1 = lowest_freq_node(forest)
t2 = lowest_freq_node(forest)
new_node = Huffman_Node(t1.freq + t2.freq)
new_node.left = t1
new_node.right = t2