def compute_bad_character_table(pattern: str) -> dict:
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table

def compute_good_suffix_table(pattern: str) -> list[int]:
    m = len(pattern)
    shift = [0] * m
    border_pos = [0] * (m + 1)

    i = m
    j = m + 1
    border_pos[i] = j

    # Faza 1: wyznaczanie tablicy border_pos
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1 if j - 1 < m else m - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    # Faza 2: wypełnianie brakujących przesunięć
    j = border_pos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border_pos[j]

    return shift[1:]  # Pomijamy pierwszą wartość, bo ona nie jest używana

def boyer_moore_pattern_match(text: str, pattern: str) -> list[int]:
    if not pattern or not text or len(pattern) > len(text):
        return []

    bad_char = compute_bad_character_table(pattern)
    good_suffix = compute_good_suffix_table(pattern)

    m = len(pattern)
    n = len(text)
    occurrences = []
    s = 0  # offset wzorca w tekście

    while s <= n - m:
        j = m - 1

        # Porównuj od końca wzorca
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            occurrences.append(s)
            s += good_suffix[0] if m > 1 else 1
        else:
            bc_shift = j - bad_char.get(text[s + j], -1)
            gs_shift = good_suffix[j] if j < len(good_suffix) else 1
            s += max(bc_shift, gs_shift)

    returnoccurrences
