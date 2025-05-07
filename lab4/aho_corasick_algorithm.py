from collections import deque
from typing import List, Tuple, Optional, Dict


class AhoCorasickNode:
    def __init__(self):
        """Initialize a node in the Aho-Corasick trie."""
        self.transitions: Dict[str, 'AhoCorasickNode'] = {}
        
        self.failure: Optional['AhoCorasickNode'] = None
        
        self.outputs: List[str] = []
        
        self.is_terminal: bool = False


class AhoCorasick:
    def __init__(self, patterns: List[str]):
        """
        Initialize the Aho-Corasick automaton with the given patterns.
        
        Args:
            patterns: List of patterns to search for
        """
        self.patterns = [pattern for pattern in patterns if pattern]
        
        self.root = AhoCorasickNode()
        
        self._build_trie()
        
        self._build_failure_links()

    def _build_trie(self):
        """Builds the trie structure for the given patterns."""
        for pattern in self.patterns:
            current = self.root
            
            for char in pattern:
                if char not in current.transitions:
                    current.transitions[char] = AhoCorasickNode()
                
                current = current.transitions[char]
            
            current.is_terminal = True
            current.outputs.append(pattern)

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        queue = deque()
        
        for char, node in self.root.transitions.items():
            node.failure = self.root
            queue.append(node)
        
        while queue:
            current = queue.popleft()
            
            for char, child in current.transitions.items():
                queue.append(child)
                
                failure_node = current.failure
                
                while failure_node is not self.root and char not in failure_node.transitions:
                    failure_node = failure_node.failure
                
                if char in failure_node.transitions:
                    child.failure = failure_node.transitions[char]
                else:
                    child.failure = self.root
                
                child.outputs.extend(child.failure.outputs)

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        results = []
        current = self.root
        
        for i, char in enumerate(text):
            while current is not self.root and char not in current.transitions:
                current = current.failure
            
            if char in current.transitions:
                current = current.transitions[char]
                
                for pattern in current.outputs:
                    start_index = i - len(pattern) + 1
                    results.append((start_index, pattern))
        
        return results
