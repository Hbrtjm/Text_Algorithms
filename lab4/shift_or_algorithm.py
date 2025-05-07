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
    return (m >> n) & 1  


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    masks = [0xff] * 256
    
    for i, char in enumerate(pattern):
        masks[ord(char)] &= ~set_nth_bit(i)
    
    return masks

def shift_or(text: str, pattern: str) -> list[int]:
    """
    Implementacja algorytmu Shift-Or do wyszukiwania wzorca.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
    """
    n = len(text)
    m = len(pattern)
    result = []
    if n == 0 or m == 0 or n < m:
        return result
    masks = make_mask(pattern)
    state = ~0
    result = []

    for i, ch in enumerate(text):
        state = (state << 1) | masks[ord(ch)]
        if nth_bit(state, m - 1) == 0:
            result.append(i - m + 1)

    return result

