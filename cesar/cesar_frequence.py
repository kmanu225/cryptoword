from utils import ord_e, get_frequences, striper
from cesar_bruteforce import rot_left, rot_right

get_cesar_key = lambda frequence: ord(list(frequence.keys())[0]) - ord_e

decrypt_cesar = lambda cyphertext: rot_left(
    cyphertext, get_cesar_key(get_frequences(cyphertext))
)


if __name__ == "__main__":
    cypher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    cypher_text = striper(cypher_text)
    print(decrypt_cesar(cypher_text))
