def compute_z_array(s: str) -> list[int]:
    """
    Compute the Z array for a string.

    The Z array Z[i] gives the length of the longest substring starting at position i
    that is also a prefix of the string.

    Args:
        s: The input string

    Returns:
        The Z array for the string
    """
    # TODO: Implement the Z-array computation
    # For each position i:
    # - Calculate the length of the longest substring starting at i that is also a prefix of s
    # - Use the Z-box technique to avoid redundant character comparisons
    # - Handle the cases when i is inside or outside the current Z-box
    n = len(s)
    def len_of_common_prefix(s1, s2):
        length = 0
        while length < len(s1) and length < len(s2) and s1[length] == s2[length]:
            length += 1
        return length

    z = [0] * n
    l = 0
    r = 0
    for k in range(1, n):
        if k >= r:
            z[k] = len_of_common_prefix(s[k:], s)
            if z[k] > 0:
                l = k
                r = k + z[k]
        elif z[k - l] >= r - k:
            z[k] = r - k + len_of_common_prefix(s[r:], s[r - k:])
            l = k
            r = k + z[k]
        else:
            z[k] = z[k - l]
    return z


def z_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Use the Z algorithm to find all occurrences of a pattern in a text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement pattern matching using the Z algorithm
    # 1. Create a concatenated string: pattern + special_character + text
    # 2. Compute the Z array for this concatenated string
    # 3. Find positions where Z[i] equals the pattern length
    # 4. Convert these positions in the concatenated string to positions in the original text
    # 5. Return all positions where the pattern is found in the text
    result = []
    n = len(text)
    m = len(pattern)
    if n == 0 or m == 0 or n < m:
        return result
    concatinated = f"{pattern}*{text}"
    Z = compute_z_array(concatinated)
    for i in range(m + 1, len(concatinated)):
        if Z[i] == m:
            result.append(i - m - 1)
    return result
