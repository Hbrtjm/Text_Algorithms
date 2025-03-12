# 1. Poprosi użytkownika o wprowadzenie ciągu znaków (np. słowa lub zdania)
# 2. Policzy częstotliwość występowania każdego znaku w tekście
# 3. Wyświetli znaki w kolejności od najczęściej do najrzadziej występujących wraz z liczbą wystąpień
# 4. Sprawdzi, czy tekst jest anagramem (czy można z niego utworzyć inne słowo używając dokładnie tych samych liter)
# z podanym przez użytkownika drugim słowem lub frazą

def task3():
    text = input('Podaj tekst: ')
    
    def count_chars(string):
        chars = dict()
        for c in string:
            if c not in chars:
                chars[c] = 1
            else:
                chars[c] += 1
        return chars
    text = text.replace(' ', '')
    text_chars = count_chars(text)
    text_chars = text_chars
    print(f"Texts chars {text_chars}")

    # chars_counts_sorted = list(zip(*text_chars.keys(),*text_chars.values())).sort(key=lambda x,y: x[1] > y[1])
    chars_counts_sorted = sorted(text_chars.items(), key=lambda x: x[1],reverse=True)
    print(f"Sorted text chars {chars_counts_sorted}")

    text2 = input('Podaj drugi tekst: ')
    text2 = text2.replace(' ', '')
    def is_anagram(string1,string2):
        if len(string1) != len(string2):
            return False
        c1 = count_chars(string1)
        c2 = count_chars(string2)
        for c in string1:
            if c not in c2 or c1[c] != c2[c]:            
                return False
        return True
    print("Jest anagramem" if is_anagram(text,text2) else "Nie jest anagramem")
    


if __name__ == "__main__":
    task3()
