def rabin_karp_pattern_match(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Implementation of the Rabin-Karp pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for
        prime: A prime number used for the hash function

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement the Rabin-Karp string matching algorithm
    # This algorithm uses hashing to find pattern matches:
    # 1. Compute the hash value of the pattern
    # 2. Compute the hash value of each text window of length equal to pattern length
    # 3. If the hash values match, verify character by character to avoid hash collisions
    # 4. Use rolling hash to efficiently compute hash values of text windows
    # 5. Return all positions where the pattern is found in the text
    # Note: Use the provided prime parameter for the hash function to avoid collisions
    result = []
    n = len(text)
    m = len(pattern)
    if n < m or n == 0 or m == 0:
        return result
    
    def hasha(s: str, base: int = 256, prime: int = 101) -> int:
        h = 0
        for char in s:
            h = (h * base + ord(char)) % prime
        return h

    hashes = []
    pattern_hash = hasha(pattern)

    for i in range(n):
        hashes.append(hasha(text[i:(i+m)]))

    for i, substr_hash in enumerate(hashes):
        if substr_hash == pattern_hash:
            result.append(i)
    return result
