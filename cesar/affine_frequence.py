from utils import alphabet, ord_a, get_frequences, striper

def get_affine_key(frequence):
    ordered_frequence = sorted(frequence.items(), key=lambda x: x[1], reverse=True)
    firt_max = ord(ordered_frequence[0][0]) - ord_a
    second_max = ord(ordered_frequence[1][0]) - ord_a

    ord_e = ord("e") - ord_a
    ord_t = ord("t") - ord_a # la deuxième lettre la plus fréquente en français varie entre 'a', 't', ..

    a = (second_max - firt_max) * pow(ord_t - ord_e, -1, 26) % 26
    b = (firt_max - a * ord_e) % 26
    return (a, b)


def affine_cypher(text, key):
    result = ""
    for i in range(len(text)):
        if text[i] in alphabet:
            result += alphabet[(key[0] * alphabet.index(text[i]) + key[1]) % 26]
        else:
            result += text[i]
    return result


def affine_decypher(text, key):
    result = ""
    for i in range(len(text)):
        if text[i] in alphabet:
            result += alphabet[
                (pow(key[0], -1, 26) * (alphabet.index(text[i]) - key[1])) % 26
            ]
        else:
            result += text[i]
    return result


decrypt_affine = lambda text: affine_decypher(text, get_affine_key(get_frequences(text)))


if __name__ == "__main__":
    cypher_text = "ntjmpumgxpqtstgapgtxpnchumtputgfsftgthnngxnchumwxootrtumhpyctgktjqtjchfooxujqhgztumxpotjxotfoqtohrxumhzutwftgtopfmnt jmpuatmfmshodpfrxpjjtatghbxuj"
    cypher_text = striper(cypher_text)
    print(decrypt_affine(cypher_text))
