from collections import deque

class Node:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.start = -1
        self.end = -1
        self.id = -1
 
class SuffixTree:
    def __init__(self, text: str):
        """
        Construct a suffix tree for the given text using Ukkonen's algorithm.
 
        Args:
            text: The input text for which to build the suffix tree
        """
        self.text = text + "$"
        self.root = Node()
        self.active_node = self.root
        self.active_edge = 0
        self.active_length = 0
        self.remainder = 0
        self.build_tree()
 
    def create_node(self, start, end = None, link = self.root):
        node = Node()
        node.start = start
        node.end = end
        node.suffixLink = link
        return node
    
    def build_tree(self):
        for i in range(len(self.text)):
            self.extend_tree(i)

    def extend_tree(self, pos):
        self.end = pos
        self.remainder += 1
        last_new_node = None

        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = pos

            edge_char = self.text[self.active_edge]

            # Case 1: no edge starting with active_edge char
            if edge_char not in self.active_node.children:
                leaf = Node(pos, float('inf'))
                self.active_node.children[edge_char] = leaf

                if last_new_node:
                    last_new_node.suffix_link = self.active_node
                    last_new_node = None
            else:
                # Walk down or split logic goes here
                break  # To keep this short, we’ll leave it here

            self.remainder -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    def build_tree(self):
        """
        Build the suffix tree using Ukkonen's algorithm.
        """
        remainder = 0
        for i in range(n):  # Phase i
            remainder += 1
            last_created_internal_node = None
            
            while remainder > 0:
                # Step 1: Check if the current suffix is already in the tree
                if self.root.children.find((remainder,i)):
                    remainder -= 1
                    continue
                else:
                    
                # Step 2: If not, add a new leaf or split an existing edge
                # Step 3: Use suffix links for fast traversal
                self.root.children.add(((remainder,i),new_node))
                new_node = create_node(remainder,i,self.active_node)
                # Step 4: Update active point and remainder
                remainder -= 1
                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = pos - self.remainder + 1
                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link
    
    def find_pattern(self, pattern: str) -> list[int]:
        """
        Find all occurrences of the pattern in the text.
 
        Args:
            pattern: The pattern to search for
 
        Returns:
            A list of positions where the pattern occurs in the text
        """
        # Implement pattern search using the suffix tree
        pass        
