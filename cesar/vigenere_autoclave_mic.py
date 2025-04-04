from utils import ord_a, IC_fr, IC, get_frequences, striper
from cesar_frequence import get_cesar_key
from vigenere_kasiski import vigenere_to_cesars, cesars_to_vigenere, rot_left


def transform_text(text, l):
    transformed_text = text[:l]
    n = len(text)
    for i in range(l, n):
        transformed_text += rot_left(text[i], ord(transformed_text[i - l]) - ord_a)
    return transformed_text


def extract_text(text):
    n = len(text)
    segments = dict()

    for l in range(1, 10):
        transformed_text = transform_text(text, l)
        segments_l = []

        sous_text = ""
        for i in range(l):
            t = 0
            while 2 * t * l + i < n:
                sous_text += transformed_text[2 * t * l + i]
                t += 1
            segments_l.append(sous_text)
            sous_text = ""

            t = 0
            while (2 * t + 1) * l + i < n:
                sous_text += transformed_text[(2 * t + 1) * l + i]
                t += 1
            segments_l.append(sous_text)
            sous_text = ""
        segments[l] = segments_l

    return segments


def compute_ic(text):
    segments = extract_text(text)
    ic_texts = dict()
    for l, segment in segments.items():
        ic_text = 0
        for s in segment:
            ic_text += IC(s)
        ic_text /= len(segment)
        ic_texts[l] = ic_text
    return ic_texts


def decrypt_text(cypher_text, l):
    cesars = vigenere_to_cesars(cypher_text, l)
    
    # modification du chiffré d'origine c -> d
    for j in range(l):
        cesar = cesars[j]
        new_cesars = cesar[0]
        for i in range(1, len(cesar)):
            new_cesars += rot_left(cesar[i], ord(new_cesars[-1]) - ord_a)
        cesars[j] = new_cesars

    # découpage selon la parité de la position
    cesars_evens = [cesar[::2] for cesar in cesars]
    cesars_odds = [cesar[1::2] for cesar in cesars]
    key = ""
    
    for i in range(l):
        key_odd = get_cesar_key(get_frequences(cesars_odds[i]))
        key_even = get_cesar_key(get_frequences(cesars_evens[i]))
        key += chr(key_even + ord_a)

        cesars_odds[i] = rot_left(cesars_odds[i], key_odd)
        cesars_evens[i] = rot_left(cesars_evens[i], key_even)

    for i in range(l):
        new_cesars = ""
        for j in range(len(cesars[i])):
            if j % 2 == 0:
                new_cesars += cesars_evens[i][j // 2]
            else:
                new_cesars += cesars_odds[i][j // 2]
        cesars[i] = new_cesars

    vigenere = cesars_to_vigenere(cesars)
    return vigenere


if __name__ == "__main__":
    cypher_text = "crlzfzdwkpavlfedmkeluqtztmeizcxrgqqyehplrrseeguffmfwszfdemnqtpnutldgaxuxermjrpakghwgxugnijrzyjasmapypzycpoybsgigtxvnmxhuxabywupvugelzhemmdratrflissvoftwdebigtbshchilbshgdeptxakwxeaxtpwyalztaeitlmfidzmsejauevoesswhjasmjaiulpxgnrlgiljcwyetbshmtinhulwsfrvewlweeueztrsgiuhcmehzsfvmgrqxavnnajixakkumlgjunyfucgnkmdeseeiztrhnvvhsquimfvhyjmhyjgifvqwlhiuuuepnjesydyajdxzgzhakukcczkzugttrzjmujmvhyfnwzvpdjaolrkoecmmpxwwpbwzwwutjhsavwhssldzensbqperskudgxlysrlsibycjwygwmhxgcvwsyuaqmvccmbjjmksyxsqxplbgsaivkpljgrrohlnruihgmsxqcilzcimeoiwvkingbbzrymmfiviqiydcqwflqwxlvlzw"
    cypher_text = striper(cypher_text)
    print(compute_ic(cypher_text))
    print(decrypt_text(cypher_text, 4))
