from utils import ORD_LOWER_E, get_frequences, striper
from bruteforce import rot_left

get_cesar_key = lambda frequence: ord(list(frequence.keys())[0]) - ORD_LOWER_E

decrypt_cesar = lambda ciphertext: rot_left(
    ciphertext, get_cesar_key(get_frequences(ciphertext))
)


if __name__ == "__main__":
    cipher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    cipher_text = striper(cipher_text)
    print(decrypt_cesar(cipher_text))
