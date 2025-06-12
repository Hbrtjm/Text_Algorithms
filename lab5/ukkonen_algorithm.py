"""
Zaimplementuj algorytm Ukkonena do konstruowania drzewa sufiksów.

Twoja implementacja powinna zawierać trzy kluczowe optymalizacje z algorytmu Ukkonena:
- Technika skip/count
- Reguła 3 (reguła łącza sufiksowego)
- Technika wskaźnika końcowego
Przetestuj swoją implementację na różnych tekstach i wzorcach, aby upewnić się,
że działa poprawnie. Przeanalizuj i wyjaśnij złożoność czasową swojej implementacji.

"""

class Node:
  # End == None means, that the end is the current # variable
  def __init__(self, start = -1, end = None):
    self.children : dict[str, Node]= {}
    self.suffix_link = None
    self.start = start
    self.end = end
    self.suffix_index = -1
    
  def edge_length(self, position):
    if(self.end > position):
      return position - self.start + 1
    return self.end - self.start + 1


class SuffixTree:
  def __init__(self, text: str):
    """
    Construct a suffix tree for the given text using Ukkonen's algorithm.

    Args:
        text: The input text for which to build the suffix tree
    """
    self.text = text + "$"
    self.size = len(self.text)
    self.last_new_node = None
    self.root = Node()
    self.root.suffix_link = self.root
    
    # The "active point" variable
    self.active_node = self.root # node
    self.active_edge = -1 #character
    self.active_length = 0 #position
    
    # The amount of suffixes left to consider, given last letter is #
    self.remainder = 0
    
    self.build_tree()
    self.set_suffix_index(self.root, 0)
    
  # RULE 1
  # If after an insertion from the active node = root,
  # the active length is greater than 0, then:
  # -active node is not changed
  # -active length is decremented
  # -active edge is shifted right (to the first 
  #  character of the next suffix we must insert)
  
  # RULE 2
  # If we create a new internal node OR make an inserter 
  # from an internal node, and this is not the first SUCH 
  # internal node at current step, then we link the previous
  # SUCH node with THIS one through a suffix link.

  # RULE 3
  # After an insert from the active node which is not the root node,
  # we must follow the suffix link and set the active node to the 
  # node it points to. If there is no a suffix link, 
  # set the active node to the root node. Either way, active
  # edge and active length stay unchanged.


     
  def build_tree(self):
    """
    Build the suffix tree using Ukkonen's algorithm.
    """

    # i == # varianle
    for i in range(self.size):
      
      # Increment the amount of suffixes needed to be added
      self.remainder += 1
      self.last_new_node : Node | None = None
      
      # Add all suffixes
      while(self.remainder > 0):
        # Guard in the case of inserting the entirety of previous
        # suffixes (or starting) and having to start again
        # from the # suffix letter
        if(self.active_length == 0):
          self.active_edge = i
        
        edge_character = self.text[self.active_edge]
        
        # if there IS NOT an outgoing edge labelled with edge_character
        if(edge_character not in self.active_node.children):
          # if there is no outgoing edge of the character at the current i
          # create a node of that character ending on #
          
          self.active_node.children[edge_character] = Node(start=i, end = self.size-1)
          
          # RULE 2
          if(self.last_new_node is not None):
            self.last_new_node.suffix_link = self.active_node
            self.last_new_node = None
        
        # if there IS an outgoing edge labelled with edge_character
        else:
          # By getting next_node we are considering the edge
          # between current_node and next_node
          # when it comes to starts and ends
          next_node: Node = self.active_node.children[edge_character]
          # SKIP-COUNT STEP
          # if the edge's label is shorter than current length,
          # simply skip it and continue on with next labels
          
          # active_node = X
          # active_length = 4
          # active_edge = 'a' (but its numeric, we use numbers to represent letters)
          #    ab       cdef 
          # X -----> X' -----> X''
          # length = 2
          # length < active_length we wish to skip it then, so:
          # active_edge = 'c' (but numerically)
          # active_length = 2 (we reduce it accordingly)
          # active_node = X'
          
          # From that point, we may continue our logic as before
          
          length = next_node.edge_length(i)
          if(self.active_length >= length):
            self.active_edge += length
            self.active_length -= length
            self.active_node = next_node
            continue
          
          # if current character is part of the edge 
          # (between next_nodes start and end)
          if(self.text[next_node.start + self.active_length] == self.text[i]):
            # RULE 2
            # if a new internal node was created in a previous iteration of the same phase
            # phase -> loop for given remainder
            if(self.last_new_node is not None and self.active_node != self.root):
              self.last_new_node.suffix_link = self.active_node
              self.last_new_node = None
            
            self.active_length += 1
            # Exit current phase
            break
        
          # if the current character is not on the edge
          # and none of the above happened, we have to split the node
          
          # Get the position of current character
          split_position = next_node.start + self.active_length - 1
          # And do this funky move
          # Imagine we are trying to insert 'abcd' suffix into the below example
          #    ab       cabx
          # X ----> X' ----> X''
          # we would turn that into
          #    ab        c        abxd
          # X ----> X' ----> X'' ----> X''''
          #                  | d
          #                  v
          #                  X'''
          
          # This is inserting X'' into X'
          split_node = Node(next_node.start, split_position)
          self.active_node.children[edge_character] = split_node
          # This is the  X'' to X'''
          split_node.children[self.text[i]] = Node(start=i, end = self.size-1)
          # This is updating the old X'' into X'''' (so X'' -> X'''' edge)
          next_node.start += self.active_length
          split_node.children[self.text[next_node.start]] = next_node 
          
          # RULE 2
          if(self.last_new_node is not None):
            self.last_new_node.suffix_link = split_node
            
          self.last_new_node = split_node
        
        self.remainder -= 1
        
        # RULE 1
        if(self.active_node == self.root and self.active_length > 0):
          self.active_length -= 1
          self.active_edge = i - self.remainder + 1
        
        # RULE 3
        elif(self.active_node != self.root):
          self.active_node = (
            self.active_node.suffix_link if 
            self.active_node.suffix_link is not None else 
            self.root
          )
          
  def set_suffix_index(self, node: Node, label_length):
    if not node.children:
        node.suffix_index = self.size - label_length
        # print(node.start, node.end, node.suffix_index)
    else:
        for child in node.children.values():
            edge_len = child.end - child.start + 1
            self.set_suffix_index(child, label_length + edge_len)

  
  def find_pattern(self, pattern: str) -> list[int]:
    """
    Find all occurrences of the pattern in the text.

    Args:
        pattern: The pattern to search for

    Returns:
        A list of positions where the pattern occurs in the text
    """
    m = len(pattern)
    current = self.root
    
    i = 0
    while(i < m):
      c = pattern[i]
      # Cannot continue (or even start) iterating through pattern given
      # the tree
      if(c not in current.children):
        return []
      child = current.children[c]
      child_length = child.end - child.start + 1
      proper_length = min(child_length, m - i)
      segment = self.text[child.start: child.start + proper_length]
      # Can continue with first char, but the rest does not match
      if pattern[i:i+proper_length] != segment:
        return []
      i += proper_length
      current = child
    
    # Collect results from leaves (suffix_index) through dfs
    result = []
    
    def dfs(node: Node):
      if node.suffix_index >= 0:
        result.append(node.suffix_index)
      for child in node.children.values():
        dfs(child)
        
    dfs(current)
    return sorted(result)

if __name__ == "__main__":
  def test_suffix_tree():
    cases = [
      {
        "text": "banana",
        "pattern": "ana",
        "expected": [1, 3]
      },
      {
        "text": "aaaaa",
        "pattern": "aaa",
        "expected": [0, 1, 2]
      },
      {
        "text": "abcd",
        "pattern": "bc",
        "expected": [1]
      },
      {
        "text": "mississippi",
        "pattern": "issi",
        "expected": [1, 4]
      },
      {
        "text": "abcdef",
        "pattern": "xyz",
        "expected": []
      },
      {
        "text": "x",
        "pattern": "x",
        "expected": [0]
      },
      {
        "text": "abcabcabc",
        "pattern": "abc",
        "expected": [0, 3, 6]
      },
      {
        "text": "test pattern test test pattern test",
        "pattern": "pattern",
        "expected": [5, 23]
      },
      {
        "text": "abababab",
        "pattern": "aba",
        "expected": [0, 2, 4]
      }
    ]
    
    all_passed = True

    for i, case in enumerate(cases):
      text, pattern, expected = case["text"], case["pattern"], case["expected"]
      tree = SuffixTree(text)
      result = sorted(tree.find_pattern(pattern))
      if result != expected:
        print(f"Test {i + 1} FAILED: text='{text}', pattern='{pattern}'")
        print(f"Expected: {expected}, Got: {result}")
        all_passed = False
      else:
        print(f"Test {i + 1} passed")
    
    if all_passed:
      print("ALL PASSED!")

  test_suffix_tree()
