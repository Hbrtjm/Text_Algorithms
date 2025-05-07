def hamming_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Hamminga między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Hamminga (liczba pozycji, na których znaki się różnią)
        Jeśli ciągi mają różne długości, zwraca -1
    """
    distance = 0
    if len(s1) != len(s2):
        return -1
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1
    return distance

def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    return ( m >> n ) & 1

def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    # TODO: Zaimplementuj tworzenie tablicy masek
    masks = [0xff for _ in range(256)]  # Inicjalizacja masek dla wszystkich możliwych znaków ASCII
    
    for i, char in enumerate(pattern):
        masks[ord(char)] &= ~set_nth_bit(i)  # Ustawienie odpowiedniego bitu na 0 dla znaku na pozycji i
    
    return masks

def fuzzy_shift_or(text: str, pattern: str, k: int = 2) -> list[int]:
    """
    Implementacja przybliżonego wyszukiwania wzorca przy użyciu algorytmu Shift-Or.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania
        k: Maksymalna dopuszczalna liczba różnic (odległość Hamminga)

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
        z maksymalnie k różnicami
    """
    results = []
    m = len(pattern)
    n = len(text)
    if m == 0 or n == 0 or m > n or k < 0:
        return results
    
    k = min(k, m)
    
    masks = make_mask(pattern)
    
    states = [(~0) for _ in range(k + 1)]
    
    for i in range(n):
        char_mask = masks[ord(text[i])]
        
        old_states = states.copy()
        
        for j in range(1, k + 1, -1):
            states[j] = ((states[j] << 1) | char_mask) & (states[j-1] << 1) 
        
        states[0] = (states[0] << 1) | char_mask
        
        for j in range(k+1):
            if nth_bit(states[j], m - 1) == 0:
                results.append(i - m + 1)
                
    
    return sorted(list(set(results)))
