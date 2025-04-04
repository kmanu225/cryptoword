from utils import ORD_LOWER_E, get_frequences, striper
from bruteforce import rot_left

get_cesar_key = lambda frequence: ord(list(frequence.keys())[0]) - ORD_LOWER_E

decrypt_cesar = lambda cyphertext: rot_left(
    cyphertext, get_cesar_key(get_frequences(cyphertext))
)


if __name__ == "__main__":
    cypher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    cypher_text = striper(cypher_text)
    print(decrypt_cesar(cypher_text))
