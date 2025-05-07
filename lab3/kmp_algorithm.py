from lab3.z_algorithm import compute_z_array

def compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.

    Args:
        pattern: The pattern string

    Returns:
        The LPS array
    """
    # TODO: Implement the Longest Prefix Suffix (LPS) array computation
    # The LPS array helps in determining how many characters to skip when a mismatch occurs
    # For each position i, compute the length of the longest proper prefix of pattern[0...i]
    # that is also a suffix of pattern[0...i]
    # Hint: Use the information from previously computed values to avoid redundant comparisons
    
    

    m = len(pattern)
    lps = [0] * m
    
    z = compute_z_array(pattern)
    new_z = [0] * m
    prev = 0
    for i in range(m):
        prev = max(max(0, prev), z[i])
        new_z[i] = prev
        prev -= 1
    
    i = 0
    while i < m:
        if new_z[i] == 0:
            i += 1
            continue
        start = i
        while i < m and new_z[i] != 0:
            i += 1
        end = i - 1
        while start < end:
            new_z[start], new_z[end] = new_z[end], new_z[start]
            start += 1
            end -= 1
    
    j = m - 1
    while j >= 0:
        shift = 0
        while j - shift > 0 and new_z[j - shift]:
            shift += 1
        while shift > 0:
            lps[j] = new_z[j - shift + 1]
            shift -= 1
        j -= shift + 1

    return lps

def kmp_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Knuth-Morris-Pratt pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement the KMP string matching algorithm
    # 1. Preprocess the pattern to compute the LPS array
    # 2. Use the LPS array to determine how much to shift the pattern when a mismatch occurs
    # 3. This avoids redundant comparisons by using information about previous matches
    # 4. Return all positions where the pattern is found in the text

    result = []
    n, m = len(text), len(pattern)
    if m == 0 or n == 0 or m > n:
        return result

    lps = compute_lps_array(pattern)
    i, j = 0, 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result
