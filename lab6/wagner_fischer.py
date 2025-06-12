def wagner_fischer(s1: str, s2: str,
                  insert_cost: int = 1,
                  delete_cost: int = 1,
                  substitute_cost: int = 1) -> int:
    """
    Oblicza odległość edycyjną używając algorytmu Wagnera-Fischera (programowanie dynamiczne).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        insert_cost: Koszt operacji wstawienia
        delete_cost: Koszt operacji usunięcia
        substitute_cost: Koszt operacji zamiany

    Returns:
        Odległość edycyjna z uwzględnieniem kosztów operacji
    """
    n = len(s1)
    m = len(s2)

    if n == 0:
        return m * insert_cost
    if m == 0:
        return n * delete_cost

    d = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        d[i][0] = i * delete_cost
    for j in range(1, n + 1):
        d[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[j - 1] == s2[i - 1]:
                cost_sub = 0
            else:
                cost_sub = substitute_cost

            d[i][j] = min(
                d[i - 1][j] + delete_cost,
                d[i][j - 1] + insert_cost,
                d[i - 1][j - 1] + cost_sub
            )

    return d[m][n]

def wagner_fischer_with_alignment(s1: str, s2: str) -> tuple[int, str, str]:
    """
    Oblicza odległość edycyjną i zwraca wyrównanie sekwencji.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i dwa wyrównane ciągi
        (w wyrównanych ciągach '-' oznacza lukę)
    """
    n = len(s1)
    m = len(s2)

    if n == 0:
        return m, '-' * m, s2
    if m == 0:
        return n, s1, '-' * n

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[j - 1] == s2[i - 1]:
                cost_sub = 0
            else:
                cost_sub = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost_sub 
            )

    aligned_s1 = []
    aligned_s2 = []
    i, j = m, n

    while i > 0 or j > 0:
        edit_cost = 0 if s1[j - 1] == s2[i - 1] else 1
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + edit_cost:
            aligned_s1.append(s1[j - 1])
            aligned_s2.append(s2[i - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            aligned_s1.append('-')
            aligned_s2.append(s2[i - 1])
            i -= 1
        else:
            aligned_s1.append(s1[j - 1])
            aligned_s2.append('-')
            j -= 1

    aligned_s1.reverse()
    aligned_s2.reverse()

    distance = dp[m][n]
    return distance, ''.join(aligned_s1), ''.join(aligned_s2)

def wagner_fischer_space_optimized(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną używając zoptymalizowanej pamięciowo wersji algorytmu.
    
    Złożoność pamięciowa: O(m)
    Złożoność czasowa:    O(m)

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    n = len(s1)
    m = len(s2)

    if m == 0:
        return n

    d_prev = [j for j in range(m + 1)]
    d_cur = [0] * (m + 1)

    for i in range(1, n + 1):
        d_cur[0] = i
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                cost_sub = 0
            else:
                cost_sub = 1

            d_cur[j] = min(
                d_prev[j] + 1,
                d_cur[j - 1] + 1,
                d_prev[j - 1] + cost_sub
            )
        d_prev, d_cur = d_cur, d_prev

    return d_prev[m] 
