from lab4.shift_or_algorithm import shift_or

def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    # TODO: Zaimplementuj wyszukiwanie kolumn wzorca w kolumnie tekstu
    # TODO: Dla każdej kolumny wzorca, przeszukaj kolumnę tekstu
    # TODO: Zwróć listę krotek (pozycja, indeks kolumny) dla znalezionych dopasowań
    result = []
    for i, pattern_column in enumerate(pattern_columns):
        indices = shift_or(text_column, pattern_column)
        found = [ (index,i) for index in indices ] 
        if found:
            result.extend(found)
    return result


def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    results = []

    if not text or not pattern:
        return results

    text_height = len(text)
    pattern_height = len(pattern)

    # Sprawdzanie, czy wszystkie wiersze mają taką samą długość
    if len(set(len(row) for row in text)) > 1 or len(set(len(row) for row in pattern)) > 1:
        return results

    text_width = len(text[0])
    pattern_width = len(pattern[0])

    if pattern_height > text_height or pattern_width > text_width:
        return []

    pattern_columns = []
    for j in range(pattern_width):
        column = ''.join(pattern[i][j] for i in range(pattern_height))
        pattern_columns.append(column)

    matches = {}

    for j in range(text_width):
        text_column = ''.join(text[i][j] for i in range(text_height))

        column_matches = find_pattern_in_column(text_column, pattern_columns)

        for row_pos, pattern_col in column_matches:
            col_pos = j - pattern_col

            if 0 <= col_pos < text_width - pattern_width + 1:
                key = (row_pos, col_pos)

                if key not in matches:
                    matches[key] = set()
                matches[key].add(pattern_col)

    for (row, col), matched_columns in matches.items():
        if len(matched_columns) == pattern_width:
            if all(i in matched_columns for i in range(pattern_width)):
                results.append((row, col))

    return results
