'''
The Huffman Encoding algorithm requires these steps:

  1. Using some input message, msg, produce frequency table
  2. Initialize a forest [ list of Huffman Nodes ] with each Huffman Node as sym -> freq, left & right children
      3. Build a tree, while there are enough nodes in the forest:
          a. iterate through the frequencies of the Huffman nodes and find the minimum frequency node
          b. remove that node from the forest, min_freq_node1
          c. repeat a, b for another node, min_freq_node2
          d. combine the frequencies, freq1 and freq2, of min_freq_node1 and min_freq_node2 and create a root node as null -> freq1 + freq2
          e. set the freq1 as the left child of root, and freq2 as the right child of root
          f. add the root back in the forest, and continue
          d. return the root of the tree, forest[0]
      4. Using the finished tree, build an encoding table (dict):
            Perform DFS - Recursive
          a. Base Case: If the table is already null, return empty dict
          b. Recursive: The root is not null, then if the node has an assigned symbol, assign a list of '1's and '0's, LR_path, return table
          c. continue to iterate through left and right children of that node and append a '0' for the LR_path left path, and a '1' for right path
          d. return table
    5. Construct the encoded message using the encoding table:
          a. iterate through each letter of the msg
          b. concatenate the LR_path into a large encoded msg
          c. return the encoded msg
    6. Generate the report:
        - input str length
        - 8-bit storage
        - encoded str length
        - net compression
    7. Decode the encoded message using the encoding table and the encoded msg:
        a. iterate through the each bit in LR_path
        b. then iterate through key value pairs in the encoding table, 
        c. if the LR_path is a corresponding path from the bit
        d. concate the letters as the decoded msg, decode_msg
        e. return the decode_msg


'''
class Huffman_Node: # Huffman node stores freq, sym, left  & right children
    """Plain node suitable for binary trees. The node stores a frequency and a
    symbol. When no symbol is given, the node considers it null, and stores only
    the frequency."""

    # Constructor
    def __init__(self, frequency, symbol=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

def frequencies_dict(message: str) -> dict: # Frequency table method
    """Returns the symbol frequency of a string as a dictionary."""
    frequency = dict()  # Initialize a dictionary
    if message is not None and len(message) > 0:  # Input not null and not empty
        for symbol in message:  # For every symbol in the string
            if symbol in frequency:  # If symbol already in dictionary
                frequency[symbol] += 1  # increase frequency for this symbol
            else:  # Symbol not in dictionary yet
                frequency[symbol] = 1  # Initialize frequency for this symbol
    return frequency  # Done

def initialize_forest(freq_table): # Initializing forest method
    forest = [] # forest stores the Huffman nodes
    for sym, freq in freq_table.items(): # for every symbol and freq in the table
        forest_node = Huffman_Node(freq, sym) # make a new node, forest_node
        forest.append(forest_node) # add it to the forest
    return forest # return forest

def build_Huffman_tree(forest): # Building the tree method
    while len(forest) > 1: # while there is at least one node in the node
        
        min_freq_node1 = min(forest, key=lambda x: x.frequency) 
        # find the minimum freq node in the forest
        forest.remove(min_freq_node1) # remove it, and save

        # again
        min_freq_node2 = min(forest, key=lambda x: x.frequency)
        forest.remove(min_freq_node2)

        # add the frequencies of the two minimum nodes
        combined_freq = min_freq_node1.frequency + min_freq_node2.frequency
        root = Huffman_Node(combined_freq) # create a new node with the combined freq, with null symbol
        root.left = min_freq_node1 # assign the first minimum freq node as the left child
        root.right = min_freq_node2 # assign the other minimum freq node as the right child

        forest.append(root) # add the root of the subtree

    return forest[0] # return the root

def generate_encoding_table_DFS(Huffman_tree_root, LR_path='', encoding_table=None): # encoding table - DFS method
    
    if encoding_table is None: # if there is no encoding table, return it
        encoding_table = {}

    if Huffman_tree_root.symbol is not None: # else root is not null
        encoding_table[Huffman_tree_root.symbol] = LR_path # assign the path to the corresponding symbol
        return encoding_table # return the table

    # recursively iterate left, add 0 to path, update encoding table
    encoding_table = generate_encoding_table_DFS(Huffman_tree_root.left, LR_path + '0', encoding_table)
    # recursively iterate right, add 1 to path, update encoding table
    encoding_table = generate_encoding_table_DFS(Huffman_tree_root.right, LR_path + '1', encoding_table)
    return encoding_table # return the encoding table

def Huffman_code_generation(encoding_table, msg): # encoding in bits method
    encoded_msg = '' # encoded_msg stores the encoded message of bits
    for letter in msg: # for every letter in the original msg
        encoded_msg += encoding_table[letter] # add the bits of the path of the letter
    return encoded_msg # return the encoded message

def generate_compression_report(encoded_msg, msg): # generate report
    msg_len = len(msg)
    storage_req = 8 * msg_len
    encoded_msg_len = len(encoded_msg)
    net_compression = 100 * (1 - (encoded_msg_len / storage_req))

    print("Input string length:", msg_len, "characters")
    print("8-bit storage required:", storage_req, "bits")
    print("Encoded string length:", encoded_msg_len, "bits")
    print("Net compression:", net_compression, "%")

def decoded_Huffman_encrypted_msg(encoded_msg, encoding_table): # decode encoded message
    decoded_msg = '' # decoded_msg stores the decoded mesage of letters
    LR = '' # bit group of letter
    for bit in encoded_msg: # for every bit in the encoded msg
        LR += bit # add to the bit group
        for letter, LR_path in encoding_table.items(): 
            # for the letters of the original msg, and their LR_path
            if LR_path == LR: # if the bit group matched the LR_path of an assigned letter
                decoded_msg += letter # concatanate the letter
                LR = '' # reset bit group
                break # finish, we found a letter
            
    return decoded_msg # return the decoded message

def main():
    msg = "HELLO WORLD"
    freq_dict = frequencies_dict(msg)
    forest = initialize_forest(freq_dict)
    Huffman_tree = build_Huffman_tree(forest)
    encoding_table = generate_encoding_table_DFS(Huffman_tree)
    encoded_msg = Huffman_code_generation(encoding_table, msg)

    print("Original message:", msg)
    print("Encoded message:", encoded_msg)
    print("Encoding table:", encoding_table)
    generate_compression_report(encoded_msg, msg)

    print("Let's decode....")
    decoded_msg = decoded_Huffman_encrypted_msg(encoded_msg, encoding_table)

    if decoded_msg == msg:
        print("Encoded message -> Original message: Success!")
    else:
        print("Decoding failed.")

main()
