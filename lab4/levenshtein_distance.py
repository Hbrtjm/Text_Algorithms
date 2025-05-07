def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    # TODO: Zaimplementuj obliczanie odległości Levenshteina
    # TODO: Obsłuż przypadki brzegowe (puste ciągi)
    # TODO: Zaimplementuj algorytm dynamicznego programowania do obliczenia odległości
    def tail(s):
        return s[1:]
    def head(s):
        return s[0]

    if len(s1) == 0:
        return len(s2)
    
    if len(s2) == 0:
        return len(s1)
    
    if head(s2) == head(s1):
        return levenshtein_distance(tail(s1),tail(s2))
    
    return 1 + min(levenshtein_distance(tail(s1),s2),levenshtein_distance(s1,tail(s2)),levenshtein_distance(tail(s1),tail(s2)))
