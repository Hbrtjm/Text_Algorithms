import hashlib
from typing import List, Tuple


class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """Inicjalizuje hash Nilsimsa."""
        self.result_hash = None

    def _rolling_hash(self, text: str) -> list[int]:
        """
        Oblicza rolling hash dla tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash
        """
        def hash3(trigram):
            return 256 ** 2 * ord(trigram[0]) + 256 * ord(trigram[1]) + ord(trigram[2])
        
        result = []
        n = len(text)
        
        for i in range(n):
            if i + 2 < n:
                trigram = text[i:i+3]
                result.append(hash3(trigram))
            else:
                if i < n:
                    result.append(ord(text[i]))
        
        return result

    def _trigrams(self, text: str) -> list[str]:
        """
        Generuje trigramy z tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista trigramów
        """
        n = len(text)
        result = []
        for i in range(n - 2):
            result.append(text[i] + text[i+1] + text[i+2])
        return result

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        rolling_hashes = self._rolling_hash(text)
        
        hash_bits = [0] * 256
        
        for hash_val in rolling_hashes:
            for i in range(8):
                bit_pos = (hash_val >> i) & 0xFF
                if bit_pos < 256:
                    hash_bits[bit_pos] = 1
        
        result_bytes = bytearray(32)
        for i in range(256):
            byte_idx = i // 8
            bit_idx = i % 8
            if hash_bits[i]:
                result_bytes[byte_idx] |= (1 << bit_idx)
        
        self.result_hash = bytes(result_bytes)
        return self.result_hash

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        if len(hash1) != len(hash2):
            return 0.0
        
        diff_bits = 0
        total_bits = len(hash1) * 8
        
        for b1, b2 in zip(hash1, hash2):
            xor_result = b1 ^ b2
            diff_bits += bin(xor_result).count('1')
        
        similarity = 1.0 - (diff_bits / total_bits)
        return similarity


def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    nim1 = NilsimsHash()
    nim2 = NilsimsHash()

    hash1 = nim1.compute_hash(text1)
    hash2 = nim2.compute_hash(text2)
    return nim1.compare_hashes(hash1, hash2)


def find_similar_texts(target: str, candidates: list[str], threshold: float = 0.7) -> list[tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    result = []
    
    for i, candidate in enumerate(candidates):
        similarity = nilsims_similarity(target, candidate)
        if similarity >= threshold:
            result.append((i, similarity))
    
    return result
