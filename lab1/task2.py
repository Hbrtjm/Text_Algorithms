def is_palindrome(text):
    # TODO: Usuń spacje i przekształć tekst na małe litery
    text = text.lower().replace(' ','')

    # TODO: Sprawdź, czy tekst czytany od przodu jest taki sam jak od tyłu
    # WSKAZÓWKA: Użyj notacji text[::-1] aby odwrócić tekst
    return text == text[::-1]

def make_palindrome(text):
    # Usuwamy spacje i konwertujemy do małych liter
    text = text.lower().replace(" ", "")

    # Sprawdzamy, czy już jest palindromem
    if is_palindrome(text):
        return text

    # TODO: Utwórz palindrom dodając odwrócone znaki na końcu
    # (bez ostatniego znaku, który już jest na początku odwróconego tekstu)
    option1 =  text + text[:1:-1]
    print(option1)
    # TODO: Utwórz palindrom dodając odwrócone znaki na początku
    # (bez pierwszego znaku, który już jest na końcu oryginalnego tekstu)
    option2 = text[:1:-1] + text
    print(option2)
    # TODO: Zwróć krótszą opcję jako wynik
    # W sumie są takie same
    return option2 if len(option2) < len(option1) else option1

def palindrome_checker():
    # Pobieranie danych od użytkownika
    text = input("Wprowadź słowo lub frazę: ")

    # TODO: Usuń znaki, które nie są literami ani cyframi, i zamień na małe litery
    # WSKAZÓWKA: Wykorzystaj funkcję isalnum() i list comprehension lub wyrażenie generujące
    clean_text = ''.join([ c.lower() if c.isalnum() else '' for c in text ]).lower()

    # Sprawdzanie, czy to palindrom
    if is_palindrome(clean_text):
        print(f"\"{text}\" jest palindromem!")
    else:
        print(f"\"{text}\" nie jest palindromem.")
        suggested = make_palindrome(clean_text)
        print(f"Sugerowany palindrom: {suggested}")

# Wywołanie funkcji
if __name__ == "__main__":
    palindrome_checker()