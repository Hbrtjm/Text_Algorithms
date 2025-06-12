from typing import List, Tuple


def build_suffix_array(s: str) -> List[int]:
    """
    Build the suffix array for string s using the doubling algorithm.

    Args:
        s: Input string

    Returns:
        A list SA of length len(s), where SA[i] is the starting index of the i-th smallest suffix of s.
    """
    n = len(s)
    # Initial ranking: rank[i] = ord(s[i])
    rank = [ord(c) for c in s]
    sa = list(range(n))
    tmp = [0] * n
    k = 1

    def compare(i: int, j: int) -> bool:
        # Compare pair (rank[i], rank[i+k]) vs (rank[j], rank[j+k]), where rank[x] = -1 if x >= n
        if rank[i] != rank[j]:
            return rank[i] < rank[j]
        ri = rank[i + k] if i + k < n else -1
        rj = rank[j + k] if j + k < n else -1
        return ri < rj

    while k < n:
        # Sort SA by (rank[i], rank[i+k]) using the compare function
        sa.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))
        # Build temporary array tmp with new ranks
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (1 if compare(sa[i - 1], sa[i]) else 0)
        rank[:] = tmp[:]
        k <<= 1
        if rank[sa[-1]] == n - 1:
            break

    return sa


def build_lcp(s: str, sa: List[int]) -> List[int]:
    """
    Build the LCP array for string s given its suffix array sa using Kasai's algorithm.

    Args:
        s: Input string
        sa: Suffix array of s

    Returns:
        LCP array where lcp[i] = LCP(sa[i], sa[i-1]) for i in [1..n-1], and lcp[0] = 0.
    """
    n = len(s)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] == 0:
            lcp[0] = 0
            continue
        j = sa[rank[i] - 1]
        # Compute LCP between suffixes at i and j
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rank[i]] = h
        if h > 0:
            h -= 1
    return lcp


def longest_common_substring(str1: str, str2: str) -> str:
    """
    Find the longest common substring of two strings using a suffix array.

    Args:
        str1: First string
        str2: Second string

    Returns:
        The longest common substring
    """
    # Concatenate with unique separators
    sep1 = "#"
    sep2 = "$"
    combined = str1 + sep1 + str2 + sep2
    n1 = len(str1)
    n2 = len(str2)
    n = len(combined)

    # Build suffix array and LCP array
    sa = build_suffix_array(combined)
    lcp = build_lcp(combined, sa)

    max_len = 0
    pos = 0
    for i in range(1, n):
        i1 = sa[i]
        i2 = sa[i - 1]
        # Check if the two suffixes originate from different input strings
        if (i1 < n1 and i2 > n1) or (i1 > n1 and i2 < n1):
            if lcp[i] > max_len:
                max_len = lcp[i]
                pos = sa[i]

    # Extract longest common substring
    longest_substring = combined[pos : pos + max_len]
    return longest_substring


def longest_common_substring_multiple(strings: List[str]) -> str:
    """
    Find the longest common substring among multiple strings using a generalized suffix array.

    Args:
        strings: List of input strings

    Returns:
        The longest common substring that appears in all strings
    """
    # Concatenate all strings with unique separators
    # Use ASCII values starting from 1, 2, ..., which do not appear in any string.
    # We'll map each string to an integer ID [0..k-1].
    k = len(strings)
    if k == 0:
        return ""
    if k == 1:
        return strings[0]

    # Build combined string
    combined = []
    origin = []
    sep_ord = 1
    for idx, s in enumerate(strings):
        for c in s:
            combined.append(c)
            origin.append(idx)
        combined.append(chr(256 + sep_ord))  # Unique separator beyond standard ASCII
        origin.append(-1)
        sep_ord += 1

    combined_str = "".join(combined)
    n = len(combined_str)

    # Build suffix array and LCP
    sa = build_suffix_array(combined_str)
    lcp = build_lcp(combined_str, sa)

    # Sliding window over SA to find interval containing at least one suffix from each origin
    # Use two pointers and a counter array
    result_len = 0
    result_pos = 0

    from collections import Counter

    count = Counter()
    total_in_window = 0
    left = 0

    def get_origin(i: int) -> int:
        return origin[i]

    for right in range(n):
        orig_r = get_origin(sa[right])
        if orig_r != -1:
            count[orig_r] += 1
            if count[orig_r] == 1:
                total_in_window += 1

        # If window includes all k origins, try to shrink from left
        while total_in_window == k and left <= right:
            # Compute minimum LCP in [left+1..right]
            if left < right:
                min_lcp = min(lcp[left + 1 : right + 1])
                if min_lcp > result_len:
                    result_len = min_lcp
                    result_pos = sa[right]
            # Shrink window from left
            orig_l = get_origin(sa[left])
            if orig_l != -1:
                count[orig_l] -= 1
                if count[orig_l] == 0:
                    total_in_window -= 1
            left += 1

    if result_len == 0:
        return ""
    return combined_str[result_pos : result_pos + result_len]


def longest_palindromic_substring(text: str) -> str:
    """
    Find the longest palindromic substring in a given text using suffix array.

    Args:
        text: Input text

    Returns:
        The longest palindromic substring
    """
    n = len(text)
    if n == 0:
        return ""

    # Create a string: T + '#' + reverse(T) + '$'
    rev = text[::-1]
    sep = "#"
    end = "$"
    combined = text + sep + rev + end

    # Build suffix array and LCP
    sa = build_suffix_array(combined)
    lcp = build_lcp(combined, sa)
    total_len = len(combined)

    max_len = 0
    pos = 0

    for i in range(1, total_len):
        i1 = sa[i]
        i2 = sa[i - 1]
        # Check that one suffix comes from the original text part, the other from the reversed part
        if (i1 < n and i2 > n) or (i1 > n and i2 < n):
            # Potential palindrome length is lcp[i]
            length = lcp[i]
            # Identify starting positions in original text
            if i1 < n:
                start1 = i1
                start2 = i2 - (n + 1)  # adjust index in reversed part
            else:
                start1 = i2
                start2 = i1 - (n + 1)
            # Check if they correspond to a palindrome:
            # In original string, the substring starting at start1 of length `length`
            # should match the reverse substring starting at (n - 1 - start2 - (length - 1)).
            # Equivalently, start1 + length - 1 == n - 1 - start2
            if start1 + length - 1 == n - 1 - start2:
                if length > max_len:
                    max_len = length
                    pos = start1

    if max_len == 0:
        # Every single character is a palindrome
        return text[0]
    return text[pos : pos + max_len]


# Example usage (for quick sanity checks):
if __name__ == "__main__":
    # Two-string LCS test
    s1 = "banana"
    s2 = "ananas"
    print(f"LCS of two strings {s1} {s2}: {longest_common_substring(s1, s2)}")  # Expected "anana" or "anana"

    # Multiple-string LCS test
    strs = ["ababc", "babca", "abcba"]
    print(f"LCS of multiple strings: {strs}, {longest_common_substring_multiple(strs)}")  # Expected "abc"

    # Longest palindromic substring test
    t = "babad"
    print("Longest palindromic substring:", longest_palindromic_substring(t))  # Expected "bab" or "aba"

