def compute_bad_character_table(pattern: str) -> dict:
    """
    Compute the bad character table for the Boyer-Moore algorithm.

    Args:
        pattern: The pattern string

    Returns:
        A dictionary with keys as characters and values as the rightmost position
        of the character in the pattern (0-indexed)
    """
    # The bad character heuristic for Boyer-Moore algorithm
    # This table maps each character to its rightmost occurrence in the pattern
    # For characters not in the pattern, they should not be in the dictionary
    # Remember that this is used to determine how far to shift when a mismatch occurs
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table


def compute_good_suffix_table(pattern: str) -> list[int]:
    """
    Compute the good suffix table for the Boyer-Moore algorithm.

    Args:
        pattern: The pattern string

    Returns:
        A list where shift[i] stores the shift required when a mismatch
        happens at position i of the pattern
    """
    # The good suffix heuristic for Boyer-Moore algorithm
    # This is a more complex rule that handles:
    # 1. When we have seen a suffix before elsewhere in the pattern
    # 2. When only a prefix of the suffix matches a prefix of the pattern
    # Hint: This involves two-phase preprocessing of the pattern
    m = len(pattern)
    shift = [0] * (m + 1)
    pos = [0] * (m + 1)

    i = m
    j = m + 1
    pos[i] = j
    
    while i > 0: 
        last_position = j - 1 if j - 1 < m else m - 1
        while j <= m and pattern[i - 1] != pattern[last_position]:
            if shift[j] == 0:
                shift[j] = j - i
            j = pos[j]
        i -= 1
        j -= 1
        pos[i] = j
    
    j = pos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = pos[j]

    return shift


def boyer_moore_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Boyer-Moore pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # Implement the Boyer-Moore string matching algorithm
    # 1. Preprocess the pattern to create the bad character and good suffix tables
    # 2. Start matching from the end of the pattern and move backwards
    # 3. When a mismatch occurs, use the maximum shift from both tables
    # 4. Return all positions where the pattern is found in the text
    result = []
    n = len(text)
    m = len(pattern)
    
    if n == 0 or m == 0 or m > n:
        return result
    
    bad_char = compute_bad_character_table(pattern)
    good_suffix = compute_good_suffix_table(pattern)
    
    i = 0

    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += good_suffix[0] if m > 1 else 1
        else:
            bc_shift = j - bad_char.get(text[i + j], -1)
            gs_shift = good_suffix[j] if j < len(good_suffix) else 1
            i += max(bc_shift, gs_shift)
    return result
