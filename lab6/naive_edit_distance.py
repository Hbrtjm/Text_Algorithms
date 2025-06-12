def naive_edit_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną między dwoma ciągami używając naiwnego algorytmu rekurencyjnego.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    n = len(s1)
    m = len(s2)
    
    if n == 0:
        return m
    
    if m == 0:
        return n

    dp = [ [0] * n ] * m

    for i in range(m):
        dp[i][0] = i

    for i in range(n):
        dp[0][i] = i

    for i in range(m):
        for j in range(n):
            if 

def naive_edit_distance_with_operations(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Oblicza odległość edycyjną i zwraca listę operacji potrzebnych do przekształcenia s1 w s2.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i listę operacji
        Operacje: "INSERT x", "DELETE x", "REPLACE x->y", "MATCH x"
    """
    pass
