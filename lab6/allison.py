
def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
    """
    Znajduje optymalne globalne wyrównanie używając algorytmu Allisona.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania i dwa wyrównane ciągi
    """
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    traceback = [[None] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i * gap_penalty
        traceback[i][0] = 'U'
    for j in range(m + 1):
        dp[0][j] = j * gap_penalty
        traceback[0][j] = 'L'

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score)
            delete = dp[i-1][j] + gap_penalty
            insert = dp[i][j-1] + gap_penalty
            dp[i][j] = max(match, delete, insert)
            if dp[i][j] == match:
                traceback[i][j] = 'D'
            elif dp[i][j] == delete:
                traceback[i][j] = 'U'
            else:
                traceback[i][j] = 'L'

    aligned_s1, aligned_s2 = "", ""
    i, j = n, m
    while i > 0 or j > 0:
        if traceback[i][j] == 'D':
            aligned_s1 = s1[i-1] + aligned_s1
            aligned_s2 = s2[j-1] + aligned_s2
            i -= 1
            j -= 1
        elif traceback[i][j] == 'U':
            aligned_s1 = s1[i-1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
            i -= 1
        else:
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[j-1] + aligned_s2
            j -= 1

    return dp[n][m], aligned_s1, aligned_s2


def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    """
    Znajduje optymalne lokalne wyrównanie (podobnie do algorytmu Smith-Waterman).

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania, dwa wyrównane ciągi oraz pozycje początku
    """
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    traceback = [[None] * (m + 1) for _ in range(n + 1)]

    max_score = 0
    max_pos = (0, 0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score)
            delete = dp[i-1][j] + gap_penalty
            insert = dp[i][j-1] + gap_penalty
            dp[i][j] = max(0, match, delete, insert)

            if dp[i][j] == match:
                traceback[i][j] = 'D'
            elif dp[i][j] == delete:
                traceback[i][j] = 'U'
            elif dp[i][j] == insert:
                traceback[i][j] = 'L'
            else:
                traceback[i][j] = None

            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    aligned_s1, aligned_s2 = "", ""
    i, j = max_pos
    end_i = i
    while i > 0 and j > 0 and dp[i][j] > 0:
        if traceback[i][j] == 'D':
            aligned_s1 = s1[i-1] + aligned_s1
            aligned_s2 = s2[j-1] + aligned_s2
            i -= 1
            j -= 1
        elif traceback[i][j] == 'U':
            aligned_s1 = s1[i-1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
            i -= 1
        elif traceback[i][j] == 'L':
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[j-1] + aligned_s2
            j -= 1

    return max_score, aligned_s1, aligned_s2, i, end_i
