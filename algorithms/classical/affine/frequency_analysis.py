LATIN_ALPHABET = "".join([chr(ord("a") + i) for i in range(26)])

def get_frequences(text):
    """
    Counts the frequency of each letter in the given text.

    Args:
        text (str): Input text (assumed lowercase and stripped of punctuation).

    Returns:
        dict: A dictionary with letters as keys and their frequency as values, sorted by frequency descending.
    """
    frequence = {}
    for letter in text:
        if letter in frequence:
            frequence[letter] += 1
        else:
            frequence[letter] = 1
    return {k: v for k, v in sorted(frequence.items(), key=lambda item: item[1], reverse=True)}


def striper(text):
    """
    Removes punctuation, whitespace, and special characters from the text and converts it to lowercase.

    Args:
        text (str): The original plaintext or ciphertext.

    Returns:
        str: Cleaned lowercase text containing only LATIN_ALPHABETic characters.
    """
    special_characters = [" ", "\n", "\t", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"', "-"]
    for char in special_characters:
        text = text.replace(char, "")
    return text.lower()


def get_affine_key(frequence):
    """
    Attempts to guess the key (a, b) for an affine cipher based on frequency analysis.

    Args:
        frequence (dict): Letter frequencies in the ciphertext.

    Returns:
        tuple: The guessed affine key (a, b), where a is coprime with 26 and b is the shift.
    """
    
    # Get the most and second most frequent letters in ciphertext
    ORD_LOWER_A = ord("a")
    ordered_frequence = sorted(frequence.items(), key=lambda x: x[1], reverse=True)
    first_max = ord(ordered_frequence[0][0]) - ORD_LOWER_A
    second_max = ord(ordered_frequence[1][0]) - ORD_LOWER_A

    ORD_LOWER_E = ord("e") - ORD_LOWER_A # First most commonly used caractere in french
    ord_t = ord("t") - ORD_LOWER_A # Second most commonly used caractere in Notre Dame de Paris (a, s, t, r). This can change according to the domain.

    # Solve the affine system to find a and b
    a = (second_max - first_max) * pow(ord_t - ORD_LOWER_E, -1, 26) % 26
    b = (first_max - a * ORD_LOWER_E) % 26
    return (a, b)


def affine_cipher(text, key):
    """
    Encrypts a message using the affine cipher.

    Args:
        text (str): Plaintext to encrypt (lowercase).
        key (tuple): The key (a, b) used in the affine cipher.

    Returns:
        str: Encrypted ciphertext.
    """
    result = ""
    for char in text:
        if char in LATIN_ALPHABET:
            index = LATIN_ALPHABET.index(char)
            result += LATIN_ALPHABET[(key[0] * index + key[1]) % 26]
        else:
            result += char
    return result


def affine_decipher(text, key):
    """
    Decrypts a message encrypted with the affine cipher.

    Args:
        text (str): Ciphertext to decrypt (lowercase).
        key (tuple): The key (a, b) used in the affine cipher.

    Returns:
        str: Decrypted plaintext.
    """
    result = ""
    a_inv = pow(key[0], -1, 26)
    for char in text:
        if char in LATIN_ALPHABET:
            index = LATIN_ALPHABET.index(char)
            result += LATIN_ALPHABET[(a_inv * (index - key[1])) % 26]
        else:
            result += char
    return result




if __name__ == "__main__":
    decrypt_affine = lambda text: affine_decipher(text, get_affine_key(get_frequences(text)))

    cipher_text = "ntjmpumgxpqtstgapgtxpnchumtputgfsftgthnngxnchumwxootrtumhpyctgktjqtjchfooxujqhgztumxpotjxotfoqtohrxumhzutwftgtopfmnt jmpuatmfmshodpfrxpjjtatghbxuj"
    
    cipher_text = striper(cipher_text)
    print(decrypt_affine(cipher_text))
