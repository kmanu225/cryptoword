from utils import LATIN_ALPHABET


def rot_right(text, decalage):
    """
    Applies a Caesar cipher shift to the right (forward in the alphabet).

    Args:
        text (str): The plaintext to encrypt (assumed lowercase).
        decalage (int): The shift amount (e.g., 3 means A -> D).

    Returns:
        str: The encrypted ciphertext.
    """
    result = ""
    for char in text:
        if char in LATIN_ALPHABET:
            new_index = (LATIN_ALPHABET.index(char) + decalage) % 26
            result += LATIN_ALPHABET[new_index]
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result


def rot_left(text, decalage):
    """
    Reverses a Caesar cipher shift to the left (backward in the alphabet).

    Args:
        text (str): The ciphertext to decrypt (assumed lowercase).
        decalage (int): The shift amount used during encryption.

    Returns:
        str: The decrypted plaintext.
    """
    result = ""
    for char in text:
        if char in LATIN_ALPHABET:
            new_index = (LATIN_ALPHABET.index(char) - decalage) % 26
            result += LATIN_ALPHABET[new_index]
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result


bruteforce_cesar = lambda cipher_text: [rot_left(cipher_text, i) for i in range(26)]


if __name__ == "__main__":
    cipher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    # cipher_text = striper(cipher_text)
    for text in bruteforce_cesar(cipher_text):
        print(f"Decalage: {bruteforce_cesar(cipher_text).index(text)}\n{text}\n\n")
