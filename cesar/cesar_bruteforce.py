from utils import alphabet, striper


def rot_right(text, decalage):
    result = ""
    for i in range(len(text)):
        if text[i] in alphabet:
            result += alphabet[(alphabet.index(text[i]) + decalage) % 26]
        else:
            result += text[i]
    return result


def rot_left(text, decalage):
    result = ""
    for i in range(len(text)):
        if text[i] in alphabet:
            result += alphabet[(alphabet.index(text[i]) - decalage) % 26]
        else:
            result += text[i]
    return result


bruteforce_cesar = lambda cypher_text: [rot_left(cypher_text, i) for i in range(26)]


if __name__ == "__main__":
    cypher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    # cypher_text = striper(cypher_text)
    for text in bruteforce_cesar(cypher_text):
        print(f"Decalage: {bruteforce_cesar(cypher_text).index(text)}\n{text}\n\n")
